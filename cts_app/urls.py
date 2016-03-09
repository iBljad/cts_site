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
    url(r'^test1$', view=views.test1, name='test1'),
    url(r'^register$', view=views.register, name='register'),
    url(r'^logout$', view=views.logout_view, name='logout'),
    url(r'^login$', view=views.login_page, name='login_page'),
    url(r'^login_view$', view=views.login_view, name='login_view'),

]
