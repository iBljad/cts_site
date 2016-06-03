from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^apply$', views.apply, name='apply'),
    # url(r'^thanks$', views.thanks, name='thanks'),
    # url(r'^create/(?P<platform_id>[0-9]+)?(?P<error>.*)$', view=views.create, name='create_err'),
    # url(r'^create?q=(?P<platform_id>[0-9]+)$', view=views.create, name='create'),
    url(r'^create$', view=views.create, name='create'),
    url(r'^search$', view=views.search, name='search'),
    url(r'^login$', view=views.login, name='login'),
    url(r'^profile/(?P<user>.*)$', view=views.profile, name='profile'),
    url(r'^profile', view=views.profile, name='profile'),
    url(r'^reqdel/(?P<req_id>[0-9]+)$', view=views.reqdel, name='reqdel'),
    url(r'^top/(?P<entity>.*)$', view=views.top, name='top'),
    url(r'^feedback', view=views.contact, name='contact'),

]

