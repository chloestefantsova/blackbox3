from re import compile as re_compile
from re import match as re_match
from re import I as re_I

from markdown import markdown

from django.db import models
from django.utils import timezone
from django.template import Template
from django.template import Context
from django.contrib.auth.models import User


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
