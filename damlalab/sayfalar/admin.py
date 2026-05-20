from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import Person, Announcement, Thesis, ThesisParticipation , Project, ProjectParticipation , Position, Professor, Student, Topic, Conference

# Monkey patch for Django 5.0.2 template bug
original_init = ChangeList.__init__

def patched_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    if not hasattr(self, 'formset'):
        self.formset = None

ChangeList.__init__ = patched_init

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'affiliation')
    search_fields = ('name', 'email')


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display  = ('full_name_display', 'title', 'email', 'is_active')
    list_filter   = ('is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    
    def full_name_display(self, obj):
        return f"{obj.title} {obj.first_name} {obj.last_name}"
    full_name_display.short_description = 'Full Name'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ('full_name_display', 'student_type', 'status', 'advisor', 'email')
    list_filter   = ('status', 'student_type', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    
    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name_display.short_description = 'Full Name'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display  = ('title', 'date', 'is_published')
    list_filter   = ('is_published', 'date')
    search_fields = ('title',)


@admin.register(Thesis)
class ThesisAdmin(admin.ModelAdmin):
    list_display  = ('title', 'status', 'start_date', 'end_date', 'is_published')
    list_filter   = ('status', 'is_published')
    search_fields = ('title', 'abstract')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('title', 'start_date', 'end_date', 'is_published')
    list_filter   = ('is_published',)
    search_fields = ('title', 'description')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display    = ('title', 'position_type', 'is_published', 'order')
    list_filter     = ('position_type', 'is_published')
    search_fields   = ('title', 'description', 'skills', 'eligibility')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display    = ('title', 'start_date', 'end_date', 'is_published')
    list_filter     = ('is_published', 'start_date')
    search_fields   = ('title', 'description')


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display    = ('name', 'date', 'location', 'is_published')
    list_filter     = ('is_published', 'date', 'location')
    search_fields   = ('name', 'location', 'description')
