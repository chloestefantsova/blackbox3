from markdown import markdown

from django.db import models
from django.utils import timezone
from django.template import Template
from django.template import Context


class Task(models.Model):

    EQUALS_CHECK = 'EQ'
    REGEX_CHECK = 'RE'

    CHECK_CHOICES = (
        (EQUALS_CHECK, 'Equals'),
        (REGEX_CHECK, 'Regex'),
    )

    title_ru = models.CharField(null=False, blank=False, max_length=256)
    title_en = models.CharField(null=False, blank=False, max_length=256)
    category = models.CharField(null=False, blank=False, max_length=256)
    cost = models.IntegerField(null=False, blank=False)
    desc_ru = models.TextField(null=False, blank=False)
    desc_en = models.TextField(null=False, blank=False)
    writeup_ru = models.TextField(null=False, blank=False)
    writeup_en = models.TextField(null=False, blank=False)
    flag = models.CharField(max_length=1024)
    is_case_insensitive_check = models.BooleanField(default=False)
    is_trimmed_check = models.BooleanField(default=False)
    check = models.CharField(null=False, blank=False, max_length=2, choices=CHECK_CHOICES)
    created_at = models.DateTimeField(null=False, blank=True)

    def get_title(self):
        return self.title_en

    def get_desc(self):
        template_vars = {}
        for file_obj in self.uploadedtask_set.all()[0].files.all():
            template_vars[file_obj.original_name.replace('.', '_')] = file_obj.get_link()
        desc = Template(self.desc_en).render(Context(template_vars))
        return markdown(desc)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.created_at = timezone.now()
        return super(Task, self).save(*args, **kwargs)
