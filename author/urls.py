from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required

from author import views


urlpatterns = patterns(
    '',

    url(r'^$', RedirectView.as_view(url=reverse_lazy('author-login'),
                                    permanent=False)),

    url(r'^login/$',
        login,
        {'template_name': 'author/login.html'},
        name='author-login'),

    url(r'^panel/$',
        login_required(function=views.PanelView.as_view(),
                       login_url=reverse_lazy('author-login')),
        name='panel'),
)
