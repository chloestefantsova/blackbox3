from __future__ import absolute_import

from os import path
from celery import shared_task
from celery import group
from celery import chain
from lzma import LZMAFile
from tarfile import open as tar_open
from json import loads as json_loads
from jsonschema import validate as json_validate
from jsonschema import ValidationError as JsonValidationError
from re import compile as re_compile
from re import search as re_search

from django.conf import settings

from author.utils import splitext_all
from author.models import UploadedTaskDeployStatus


@shared_task
def deploy_uploaded_task(uploaded_task):
    chain(format_checks.s(uploaded_task) |
          untar_task.s() |
          move_files.s() |
          group([email_docker_deployers.s(), make_task.s()])
    )()


@shared_task
def format_checks(uploaded_task):
    if not uploaded_task.is_uploaded():
        return uploaded_task
    error_status = UploadedTaskDeployStatus(
        uploaded_task=uploaded_task,
        phase=UploadedTaskDeployStatus.PHASE_FORMAT_CHECK
    )
    untarred_path, ext = splitext_all(uploaded_task.path)
    supported_exts = ['.tar.gz', '.tar.bz2', '.tar.xz', '.tar']
    if ext not in supported_exts:
        msg = 'Unsupported format "{ext}". Should be one of {supported}.'
        msg = msg.format(ext=ext, supported=', '.join(supported_exts))
        error_status.message = msg
        error_status.save()
        return uploaded_task
    tar_file = None
    if ext == '.tar.xz':
        try:
            compressed = LZMAFile(uploaded_task.path)
            tar_file = tar_open(fileobj=compressed)
        except Exception, ex:
            error_status.message = 'Error opening tar file: %s' % str(ex)
            error_status.save()
            return uploaded_task
    else:
        try:
            tar_file = tar_open(uploaded_task.path)
        except Exception, ex:
            error_status.message = 'Error opening tar file: %s' % str(ex)
            error_status.save()
            return uploaded_task
    for name in tar_file.getnames():
        if not name.startswith('task'):
            msg = ('There is a file "{filename}" that is not within "task" '
                   'directory. All files should reside within "task" '
                   'directory.')
            msg = msg.format(filename=name)
            error_status.message = msg
            error_status.save()
            return uploaded_task
    task_file_member = None
    try:
        task_file_member = tar_file.getmember('task/task.json')
    except KeyError:
        msg = ('File "task/task.json" is not found. This file must present in '
               'each uploaded task archive')
        error_status.message = msg
        error_status.save()
        return uploaded_task
    if not task_file_member.isfile():
        msg = ('File "task/task.json" is not a file, but it is expected to be '
               'a file')
        error_status.message = msg
        error_status.save()
        return uploaded_task

    task_file = tar_file.extractfile(task_file_member)
    task_json = None
    try:
        task_json = json_loads(task_file.read())
    except Exception, ex:
        msg = 'Error reading JSON object from "task/task.json": %s' % str(ex)
        error_status.message = msg
        error_status.save()
        return uploaded_task
    schema_json = None
    try:
        schema_file = file(path.join(settings.AUX_FILES_DIR,
                                     'task-schema',
                                     'v0.2',
                                     'task-schema-0.2.json'))
        schema_str = schema_file.read()
        schema_file.close()
        schema_json = json_loads(schema_str)
    except Exception, ex:
        msg = 'Error reading JSON schema file: %s' % str(ex)
        error_status.message = msg
        error_status.save()
        return uploaded_task
    try:
        json_validate(task_json, schema_json)
    except JsonValidationError, ex:
        msg = 'File "task/task.json" is incorrect: %s' % str(ex)
        error_status.message = msg
        error_status.save()
        return uploaded_task

    mentioned_files = [
        task_json['desc_ru'],
        task_json['desc_en'],
        task_json['writeup_ru'],
        task_json['writeup_en'],
    ]
    mentioned_images = []
    if 'images' in task_json:
        for image_obj in task_json['images']:
            mentioned_images.append(image_obj['filename'])
    mentioned_files += mentioned_images
    for mentioned_file in mentioned_files:
        archive_path = 'task/%s' % mentioned_file
        try:
            tar_file.getmember(archive_path)
        except KeyError:
            msg = ('The file "{filename}" mentioned in "task/task.json" '
                   'does not appear to be in the archive. Please, check '
                   'the content of the uploaded archive')
            msg = msg.format(filename=archive_path)
            error_status.message = msg
            error_status.save()
            return uploaded_task

    template_strings = {}
    for fieldname in ['desc_ru', 'desc_en', 'writeup_ru', 'writeup_en']:
        filename = task_json[fieldname]
        member = tar_file.getmember('task/%s' % filename)
        member_file = tar_file.extractfile(member)
        template_strings[filename] = member_file.read()

    existing_filenames = []
    file_re = re_compile(r'^task/(.+)$')
    for filename in tar_file.getnames():
        if filename == 'task/task.json':
            continue
        so = re_search(file_re, filename)
        if so:
            existing_filenames.append(so.group(1))

    images_filenames = mentioned_images

    tcp_ports_map = {}
    udp_ports_map = {}
    for image in task_json['images']:
        if 'tcp_ports' in image:
            tcp_ports_map[image['filename']] = image['tcp_ports']
        if 'udp_ports' in image:
            udp_ports_map[image['filename']] = image['udp_ports']

    def check_links(template_str, existing_filenames, images_filenames,
                    tcp_ports_map, udp_ports_map):
        existing_filenames, tmp_filenames = [], existing_filenames
        for filename in tmp_filenames:
            existing_filenames.append(filename.replace('.', '_'))
        images_filenames, tmp_filenames = [], images_filenames
        for filename in tmp_filenames:
            images_filenames.append(filename.replace('.', '_'))
        tcp_ports_map, tmp_ports_map = {}, tcp_ports_map
        for filename in tmp_ports_map:
            tcp_ports_map[filename.replace('.', '_')] = tmp_ports_map[filename]
        udp_ports_map, tmp_ports_map = {}, udp_ports_map
        for filename in tmp_ports_map:
            udp_ports_map[filename.replace('.', '_')] = tmp_ports_map[filename]

        temp_var_re = re_compile(r'\{\{[^}]*\}\}')
        image_var_re = re_compile(r'^.+_(?:tcp|udp)\d+$')
        temp_vars = []
        image_temp_vars = []
        so = re_search(temp_var_re, template_str)
        while so:
            temp_var = so.group()[2:-2].strip()
            if temp_var.count('.') == 0:
                temp_vars.append(temp_var)
            elif temp_var.count('.') == 1:
                image_name, image_field = temp_var.split('.')
                if image_field not in ['host', 'port']:
                    raise Exception('Unexpected image field in template '
                                    'variable reference: %s. The fields '
                                    '"host" and "port" are the only fields '
                                    'that are expected.' % temp_var)
                if not re_search(image_var_re, image_name):
                    raise Exception('Found docker-image template variable '
                                    'with unexpected ending "%s". '
                                    'Expected endings are "_tcpXXXXX" and '
                                    '"_udpXXXXX".' % image_name)
                image_temp_vars.append(image_name)
            else:
                raise Exception('Invalid template variable. '
                                'Too many dots: %s.' % temp_var)
            template_str = template_str[so.end():]
            so = re_search(temp_var_re, template_str)
        for temp_var in temp_vars:
            if temp_var not in existing_filenames:
                msg = ('Found template variable "{filename}" that '
                       'references a file that is not present in the '
                       'uploaded archive')
                raise Exception(msg.format(filename=temp_var))
        tcp_port_re = re_compile(r'^(.+)_tcp(\d+)$')
        udp_port_re = re_compile(r'^(.+)_udp(\d+)$')
        for temp_var in image_temp_vars:
            so = re_search(tcp_port_re, temp_var)
            if so:
                name = so.group(1)
                if name not in images_filenames:
                    msg = ('Found template variable "{filename}" that '
                           'references a docker image that is not present '
                           'in the uploaded archive')
                    raise Exception(msg.format(filename=name))
                port = int(so.group(2))
                if port not in tcp_ports_map[name]:
                    raise Exception('Found docker-image template variable '
                                    '"%s" that references tcp-port %s that is '
                                    'not mentioned in the corresponding '
                                    '"tcp_ports" field in "task/task.json" '
                                    'file' % (temp_var, port))
            so = re_search(udp_port_re, temp_var)
            if so:
                name = so.group(1)
                if name not in images_filenames:
                    msg = ('Found template variable "{filename}" that '
                           'references a docker image that is not present '
                           'in the uploaded archive')
                    raise Exception(msg.format(filename=name))
                port = int(so.group(2))
                if port not in udp_ports_map[name]:
                    raise Exception('Found docker-image template variable '
                                    '"%s" that references udp-port %s that is '
                                    'not mentioned in the corresponding '
                                    '"udp_ports" field in "task/task.json" '
                                    'file' % (temp_var, port))

    for filename, template_str in template_strings.iteritems():
        try:
            check_links(template_str, existing_filenames, images_filenames,
                        tcp_ports_map, udp_ports_map)
        except Exception, ex:
            msg = 'Error checking links in "{filename}" file: {content}.'
            error_status.message = msg.format(filename=filename,
                                              content=str(ex))
            error_status.save()
            return uploaded_task

    uploaded_task.format_checks_passed = True
    uploaded_task.save()

    return uploaded_task


@shared_task
def untar_task(uploaded_task):
    if not uploaded_task.is_correct():
        return uploaded_task
    return uploaded_task


@shared_task
def move_files(uploaded_task):
    if not uploaded_task.is_untarred():
        return uploaded_task
    return uploaded_task


@shared_task
def email_docker_deployers(uploaded_task):
    if not uploaded_task.has_docker_images():
        return uploaded_task
    return uploaded_task


@shared_task
def make_task(uploaded_task):
    if not uploaded_task.files_are_deployed():
        return uploaded_task
    return uploaded_task
