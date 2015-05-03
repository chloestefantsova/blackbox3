from __future__ import absolute_import

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from celery import shared_task
from celery import group
from celery import chord

from django.core.cache import cache

from reg.models import Team
from game.models import Task


@shared_task
def recalc_data(team_pk):
    workflow = chord(
        group(recalc_rating.s(),
              recalc_available_tasks.s(),
              recalc_team.s(team_pk)),
        notify_users.si()
    )
    workflow.delay()



@shared_task
def recalc_rating():
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
        line = {}
        line['team_name'] = team.name
        line['team_flag'] = team.country.flag
        line['is_school'] = team.is_school
        line['score'] = score[team.pk]
        result.append(line)
    cache.set('rating', result)


@shared_task
def recalc_available_tasks():
    queryset = Task.objects.all()
    published_pks = [task.pk for task in queryset if task.is_published()]
    queryset = Task.objects.filter(pk__in=published_pks)
    cache.set('published', queryset)


@shared_task
def recalc_team(team_pk):
    result = []
    team = Team.objects.get(pk=team_pk)
    for task in Task.objects.all():
        if task.is_solved_by(team):
            result.append(task.pk)
    cache.set('solved%d' % team_pk, result)


@shared_task
def notify_users():
    redis_publisher = RedisPublisher(facility='tasks', broadcast=True)
    message = RedisMessage('tasks')
    redis_publisher.publish_message(message)
