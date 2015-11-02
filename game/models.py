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

    desc_en = models.TextField(null=False, blank=False)
    desc_ru = models.TextField(null=False, blank=False)
    is_school = models.BooleanField(null=False, blank=True, default=False)
    send_emails = models.BooleanField(null=False, blank=True, default=False)
    country_required = models.BooleanField(null=False, blank=True, default=True)
    auth_string_length = models.PositiveIntegerField(blank=True, default=32)
    ends_at = models.DateTimeField(null=True, blank=True)

    def get_desc(self):
        if get_language().lower().startswith('ru'):
            return self.desc_ru
        return self.desc_en


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

    def __str__(self):
        return self.title_en

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
        for deployed_image in self.deployed_images.all():
            template_vars.update(deployed_image.template_var())
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
        for deployed_image in self.deployed_images.all():
            template_vars.update(deployed_image.template_var())
        writeup = Template(writeup).render(Context(template_vars))
        return markdown(writeup)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.created_at = timezone.now()
        return super(Task, self).save(*args, **kwargs)

class DeployedTaskImage(models.Model):
    task = models.ForeignKey(Task, related_name='deployed_images')
    uploaded_image = models.ForeignKey('author.UploadedTaskImage', related_name='deployed_images')
    suffix = models.CharField(max_length=1024)
    host = models.CharField(null=False, blank=False, max_length=1024)
    port = models.CharField(null=False, blank=False, max_length=5)

    def __str__(self):
        return self.uploaded_image.original_name.replace(".", "_") + "_" + self.suffix

    def template_var(self):
        return {self.uploaded_image.original_name.replace('.', '_') + "_" + self.suffix:
                    {'host': self.host, "port": self.port}}



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
