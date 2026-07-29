from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.home,                      name='home'),
    path('announcements/',                views.announcements,             name='announcements'),
    path('announcements/<slug:slug>/',    views.announcement_detail,       name='announcement_detail'),
    path('theses/',                       views.theses,                    name='theses'),
    path('theses/<slug:slug>/',           views.thesis_detail,             name='thesis_detail'),
    path('projects/',                     views.projects,                  name='projects'),
    path('projects/<slug:slug>/',         views.project_detail,            name='project_detail'),
    path('research-groups/',              views.members,                   name='research_groups'),
    path('topics/',                       views.topics,                    name='topics'),
    path('research-analysis/',            views.research_analysis,         name='research_analysis'),
    path('research-analysis/<slug:slug>/', views.research_analysis_detail, name='research_analysis_detail'),
    path('publications/',                 views.publications,              name='publications'),
    path('conferences/',                  views.conferences,               name='conferences'),
    path('activities/',                   views.activities,                name='activities'),
    path('activities/<slug:slug>/',       views.activity_detail,           name='activity_detail'),
    path('positions/',                    views.positions,                 name='positions'),
    path('contact/',                      views.contact,                   name='contact'),
    path('api/search/',                   views.api_search,                name='api_search'),
]
