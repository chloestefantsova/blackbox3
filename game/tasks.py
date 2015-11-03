from __future__ import absolute_import

import time

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from celery import shared_task
from celery import group
from celery import chain

from django.core.cache import cache

from reg.models import Team
from game.models import Task
from game.models import Answer


@shared_task
def recalc_data(team_pk, *args, **kwargs):
    workflow = chain(
        group(recalc_rating.s(),
              recalc_available_tasks.s(),
              recalc_events.s(),
              recalc_team.s(team_pk)),
        notify_users.si()
    )
    workflow.delay()


@shared_task
def recalc_all(*args, **kwargs):
    team_pks = [team.pk for team in Team.objects.all()]
    workflow = chain(
        group(recalc_rating.s(),
              recalc_available_tasks.s(),
              recalc_events.s(),
              *[recalc_team.s(pk) for pk in team_pks]),
        notify_users.si()
    )
    workflow.delay()


@shared_task
def recalc_rating(*args, **kwargs):
    result = []
    teams = Team.objects.all()
    score = {}
    for team in teams:
        score[team.pk] = 0
    tasks = Task.objects.all().select_related('answers').select_related('member')
    for task in tasks:
        visited = {}
        for team in teams:
            visited[team.pk] = False
        for answer in task.answers.all():
            if not visited[answer.member.team.pk] and answer.is_correct():
                visited[answer.member.team.pk] = True
                score[answer.member.team.pk] += task.cost
    for team in teams:
        if team.is_hidden:
            continue
        line = {}
        line['team_name'] = team.name
        line['team_flag'] = team.country.flag
        line['is_school'] = team.is_school
        line['score'] = score[team.pk]
        result.append(line)
    cache.set('rating', result, timeout=None)


@shared_task
def recalc_available_tasks(*args, **kwargs):
    queryset = Task.objects.all()
    published_pks = [task.pk for task in queryset if task.is_published()]
    queryset = Task.objects.filter(pk__in=published_pks)
    cache.set('published', queryset, timeout=None)


@shared_task
def recalc_team(team_pk, *args, **kwargs):
    result = []
    team = Team.objects.get(pk=team_pk)
    for task in Task.objects.all():
        if task.is_solved_by(team):
            result.append(task.pk)
    cache.set('solved%d' % team_pk, result, timeout=None)


@shared_task
def notify_users(*args, **kwargs):
    redis_publisher = RedisPublisher(facility='tasks', broadcast=True)
    message = RedisMessage('tasks')
    redis_publisher.publish_message(message)


@shared_task
def recalc_events(*args, **kwargs):
    answers = Answer.objects.all().select_related('task', 'member__team').order_by('pk')
    events = []
    for answer in answers:
        event = {}
        event['id'] = answer.pk
        event['time'] = int(time.mktime(answer.created_at.timetuple()))
        event['type'] = 'taskWrong'
        if answer.is_correct():
            event['type'] = 'taskCorrect'
        event['team'] = answer.member.team.name
        event['task'] = answer.task.title_en
        event['pointsDelta'] = answer.task.cost
        events.append(event)
    cache.set('events', events, timeout=None)
