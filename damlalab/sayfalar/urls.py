from django.urls import path
from . import views

urlpatterns = [
    path('',                         views.home,           name='home'),
    path('theses/',                  views.theses,         name='theses'),
    path('theses/<slug:slug>/',      views.thesis_detail,  name='thesis_detail'),
    path('projects/',                views.projects,       name='projects'),
    path('projects/<slug:slug>/',    views.project_detail, name='project_detail'),
    path('research-groups/',         views.members,        name='research_groups'),
    path('topics/',                  views.topics,         name='topics'),
    path('conferences/',             views.conferences,    name='conferences'),
    path('positions/',               views.positions,      name='positions'),
    path('contact/',                 views.contact,        name='contact'),
]
