from re import compile as re_compile
from re import match as re_match
from re import I as re_I

from markdown import markdown

from django.db import models
from django.utils import timezone
from django.template import Template
from django.template import Context
from django.contrib.auth.models import User
from django.utils.translation import get_language


class Game(models.Model):

    ends_at = models.DateTimeField(null=True, blank=True)


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

    def is_solved_by(self, team):
        for answer in self.answers.filter(member__team=team):
            if answer.is_correct():
                return True
        return False

    def is_solved(self):
        for answer in self.answers.all():
            if answer.is_correct():
                return True
        return False

    def is_published(self):
        same_cat_tasks = Task.objects.filter(category=self.category,
                                             cost__lt=self.cost)
        same_cat_tasks = same_cat_tasks.select_related('answers')
        for task in same_cat_tasks:
            if not task.is_solved():
                return False
        return True

    def check_answer(self, answer_str):
        if self.check == self.EQUALS_CHECK:
            ans = answer_str
            correct = self.flag
            if self.is_case_insensitive_check:
                ans = ans.lower()
                correct = correct.lower()
            if self.is_trimmed_check:
                ans = ans.strip()
                correct = correct.strip()
            return ans == correct
        elif self.check == self.REGEX_CHECK:
            ans = answer_str
            flags = 0
            if self.is_case_insensitive_check:
                flags |= re_I
            if self.is_trimmed_check:
                ans = ans.strip()
            return re_match(self.flag, ans, flags)
        return False

    def get_title(self):
        if get_language() in ['ru', 'ru-ru']:
            return self.title_ru
        return self.title_en

    def get_game(self):
        games = Game.objects.all()
        if len(games) != 1:
            return None
        return games[0]

    def get_desc(self):
        if get_language() in ['ru', 'ru-ru']:
            desc = self.desc_ru
        else:
            desc = self.desc_en
        template_vars = {}
        for file_obj in self.uploadedtask_set.all()[0].files.all():
            template_vars[file_obj.original_name.replace('.', '_')] = file_obj.get_link()
        for image_obj in self.uploadedtask_set.all()[0].images.all():
            if self.category == 'web' and self.cost == 100:
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp80'] = { 'host': 'sibears.ru', 'port': '11011' }
            if self.category == 'pwn' and self.cost == 500:
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp22'] = { 'host': 'sibears.ru', 'port': '11111' }
            if self.category == 'web' and self.cost == 300:
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp8081'] = { 'host': 'sibears.ru', 'port': '11211' }
            if self.category == 'crypto' and self.cost == 400 and self.title_en.startswith('Super'):
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp21435'] = { 'host': 'sibears.ru', 'port': '11311' }
            if self.category == 'web' and self.cost == 100 and self.title_en.startswith('Stored'):
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp8083'] = { 'host': 'sibears.ru', 'port': '11411' }
            if self.category == 'crypto' and self.cost == 500 and 'strong' in self.title_en.lower():
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp32154'] = { 'host': 'sibears.ru', 'port': '11511' }
            if self.category == 'web' and self.cost == 300 and 'redirect' in self.title_en.lower():
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp8082'] = { 'host': 'sibears.ru', 'port': '11611' }
            if self.category == 'joy' and self.cost == 200 and 'dark' in self.title_en.lower():
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp80'] = { 'host': 'sibears.ru', 'port': '11711' }
            if self.category == 'networks' and self.cost == 200:
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp9898'] = { 'host': 'sibears.ru', 'port': '11811' }
            if self.category == 'networks' and self.cost == 300:
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp8787'] = { 'host': 'sibears.ru', 'port': '11911' }
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp3128'] = { 'host': 'sibears.ru', 'port': '22022' }
        desc = Template(desc).render(Context(template_vars))
        return markdown(desc)

    def get_writeup(self):
        game = self.get_game()
        if game is None or game.ends_at <= timezone.now():
            return ''
        if get_language() in ['ru', 'ru-ru']:
            writeup = self.writeup_ru
        else:
            writeup = self.writeup_en
        template_vars = {}
        for file_obj in self.uploadedtask_set.all()[0].files.all():
            template_vars[file_obj.original_name.replace('.', '_')] = file_obj.get_link()
        for image_obj in self.uploadedtask_set.all()[0].images.all():
            if self.category == 'web' and self.cost == 100:
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp80'] = { 'host': 'sibears.ru', 'port': '11011' }
            if self.category == 'pwn' and self.cost == 500:
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp22'] = { 'host': 'sibears.ru', 'port': '11111' }
            if self.category == 'web' and self.cost == 300:
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp8081'] = { 'host': 'sibears.ru', 'port': '11211' }
            if self.category == 'crypto' and self.cost == 400 and self.title_en.startswith('Super'):
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp21435'] = { 'host': 'sibears.ru', 'port': '11311' }
            if self.category == 'web' and self.cost == 100 and self.title_en.startswith('Stored'):
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp8083'] = { 'host': 'sibears.ru', 'port': '11411' }
            if self.category == 'crypto' and self.cost == 500 and 'strong' in self.title_en.lower():
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp32154'] = { 'host': 'sibears.ru', 'port': '11511' }
            if self.category == 'web' and self.cost == 300 and 'redirect' in self.title_en.lower():
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp8082'] = { 'host': 'sibears.ru', 'port': '11611' }
            if self.category == 'joy' and self.cost == 200 and 'dark' in self.title_en.lower():
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp80'] = { 'host': 'sibears.ru', 'port': '11711' }
            if self.category == 'networks' and self.cost == 200:
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp9898'] = { 'host': 'sibears.ru', 'port': '11811' }
            if self.category == 'networks' and self.cost == 300:
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp8787'] = { 'host': 'sibears.ru', 'port': '11911' }
                template_vars[image_obj.original_name.replace('.', '_')+'_tcp3128'] = { 'host': 'sibears.ru', 'port': '22022' }
        writeup = Template(writeup).render(Context(template_vars))
        return markdown(writeup)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.created_at = timezone.now()
        return super(Task, self).save(*args, **kwargs)


class Answer(models.Model):

    task = models.ForeignKey(Task, related_name='answers')
    member = models.ForeignKey('reg.Member', related_name='answers')
    flag = models.CharField(null=False, blank=False, max_length=1024)
    created_at = models.DateTimeField(null=False, blank=True)

    def is_correct(self):
        return self.task.check_answer(self.flag)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.created_at = timezone.now()
        return super(Answer, self).save(*args, **kwargs)
