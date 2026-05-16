from django.contrib import admin
from .models import Person, Announcement, Thesis, ThesisParticipation , Project, ProjectParticipation , Position, Professor, Student, Topic, Conference

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'affiliation')
    search_fields = ('name', 'email')


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display  = ('get_full_name', 'title', 'email', 'is_active')
    list_filter   = ('is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('title', 'first_name', 'last_name', 'email', 'image')
        }),
        ('Professional', {
            'fields': ('biography', 'avesis_link', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.title} {obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ('get_full_name', 'student_type', 'status', 'advisor', 'email')
    list_filter   = ('status', 'student_type', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'advisor')
        }),
        ('Academic Status', {
            'fields': ('student_type', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display  = ('title', 'date', 'is_published')
    list_filter   = ('is_published', 'date')
    search_fields = ('title',)


class ThesisParticipationInline(admin.TabularInline):
    model               = ThesisParticipation
    extra               = 1
    autocomplete_fields = ['person']


@admin.register(Thesis)
class ThesisAdmin(admin.ModelAdmin):
    list_display  = ('title', 'status', 'start_date', 'end_date', 'is_published')
    list_filter   = ('status', 'is_published')
    search_fields = ('title', 'abstract')
    inlines       = [ThesisParticipationInline]

    filter_horizontal = ('students', 'supervisors', 'principal_investigators')

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'status',
                'start_date', 'end_date',
                'image', 'pdf', 'abstract',
                'link', 'is_published',
            )
        }),
        ('Participants', {
            'fields': ('students', 'supervisors', 'principal_investigators'),
            'description': 'Select Students from Student table and Professors for supervisor/PI roles.'
        }),
    )


class ProjectParticipationInline(admin.TabularInline):
    model               = ProjectParticipation
    extra               = 1
    autocomplete_fields = ['person']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('title', 'start_date', 'end_date', 'is_published')
    list_filter   = ('is_published',)
    search_fields = ('title', 'description')
    inlines       = [ProjectParticipationInline]
    filter_horizontal = ('students', 'supervisors', 'principal_investigators')
    
    fieldsets     = (
        (None, {
            'fields': (
                'title',
                'start_date', 'end_date',
                'image', 'description',
                'link', 'is_published',
            )
        }),
        ('Participants', {
            'fields': ('students', 'supervisors', 'principal_investigators'),
            'description': 'Select Students from Student table and Professors for supervisor/PI roles.'
        }),
    )
    
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display    = ('title', 'position_type', 'is_published', 'order')
    list_filter     = ('position_type', 'is_published')
    search_fields   = ('title', 'description', 'skills', 'eligibility')
    list_editable  = ('is_published', 'order')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'position_type', 'is_published', 'order'
            )
        }),
        ('Details', {
            'fields': (
                'description', 'eligibility', 'skills', 'commitment', 'contact_email'
            )
        }),
        ('Application', {
            'fields': (
                'apply_link',
            )
        }),
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display    = ('title', 'start_date', 'end_date', 'is_published')
    list_filter     = ('is_published', 'start_date')
    search_fields   = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('students', 'supervisors', 'principal_investigators')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'start_date', 'end_date', 'image', 'link', 'is_published')
        }),
        ('Content', {
            'fields': ('description',)
        }),
        ('Participants', {
            'fields': ('students', 'supervisors', 'principal_investigators'),
            'description': 'Select Students from Student table and Professors for supervisor/PI roles.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display    = ('name', 'date', 'location', 'is_published')
    list_filter     = ('is_published', 'date', 'location')
    search_fields   = ('name', 'location', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'date', 'location', 'image', 'is_published')
        }),
        ('Details', {
            'fields': ('link', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
