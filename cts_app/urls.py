from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^apply$', views.apply, name='apply'),
    # url(r'^thanks$', views.thanks, name='thanks'),
    url(r'^create/(?P<platform_id>[0-9]+)?(?P<error>.*)$', view=views.create, name='create_err'),
    url(r'^create/(?P<platform_id>[0-9]+)$', view=views.create, name='create'),
    url(r'^apply$', views.apply, name='apply'),
    url(r'^search$', view=views.search, name='search'),
    url(r'^result$', view=views.result, name='result'),
    url(r'^quicksearch$', view=views.quicksearch, name='quicksearch'),

]
