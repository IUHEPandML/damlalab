from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Person, Announcement, AnnouncementLink, Thesis, ThesisParticipation, Project, Position, Professor, Student, Topic, Conference, ResearchAnalysis, Publication, Activity, ActivityImage

@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    list_display  = ('name', 'email', 'affiliation')
    search_fields = ('name', 'email')


@admin.register(Professor)
class ProfessorAdmin(ImportExportModelAdmin):
    list_display  = ('full_name_display', 'title', 'email', 'is_active')
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

    def full_name_display(self, obj):
        return f"{obj.title} {obj.first_name} {obj.last_name}"
    full_name_display.short_description = 'Full Name'


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display  = ('full_name_display', 'student_type', 'status', 'advisor', 'department', 'grade', 'email')
    list_filter   = ('status', 'student_type', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'department', 'grade')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'advisor')
        }),
        ('Academic Status', {
            'fields': ('student_type', 'status', 'department', 'grade')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name_display.short_description = 'Full Name'


class AnnouncementLinkInline(admin.TabularInline):
    model = AnnouncementLink
    extra = 1


@admin.register(Announcement)
class AnnouncementAdmin(ImportExportModelAdmin):
    list_display  = ('title', 'date', 'is_published', 'nonstop', 'expires_at')
    list_filter   = ('is_published', 'date', 'nonstop')
    search_fields = ('title', 'short_info', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines       = [AnnouncementLinkInline]


class ThesisParticipationInline(admin.TabularInline):
    model               = ThesisParticipation
    extra               = 1
    autocomplete_fields = ['person']


@admin.register(Thesis)
class ThesisAdmin(ImportExportModelAdmin):
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


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    list_display  = ('title', 'project_level', 'institution', 'start_date', 'end_date', 'is_published')
    list_filter   = ('project_level', 'is_published')
    search_fields = ('title', 'description')
    filter_horizontal = ('students', 'supervisors', 'principal_investigators')

    fieldsets     = (
        (None, {
            'fields': (
                'title',
                'project_level', 'institution',
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
class PositionAdmin(ImportExportModelAdmin):
    list_display    = ('title', 'position_type', 'is_published', 'order')
    list_filter     = ('position_type', 'is_published')
    search_fields   = ('title', 'description', 'skills', 'eligibility')
    list_editable   = ('is_published', 'order')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'position_type', 'image', 'is_published', 'order'
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
class TopicAdmin(ImportExportModelAdmin):
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
class ConferenceAdmin(ImportExportModelAdmin):
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


@admin.register(ResearchAnalysis)
class ResearchAnalysisAdmin(ImportExportModelAdmin):
    list_display    = ('title', 'category', 'order', 'is_published')
    list_filter     = ('category', 'is_published', 'created_at')
    search_fields   = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('students', 'supervisors', 'principal_investigators')


@admin.register(Publication)
class PublicationAdmin(ImportExportModelAdmin):
    list_display    = ('title', 'publication_type', 'year', 'supervisor', 'is_published')
    list_filter     = ('publication_type', 'year', 'is_published', 'created_at')
    search_fields   = ('title', 'authors', 'venue', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')


class ActivityImageInline(admin.TabularInline):
    model = ActivityImage
    extra = 1


@admin.register(Activity)
class ActivityAdmin(ImportExportModelAdmin):
    list_display    = ('title', 'category', 'start_date', 'end_date', 'location', 'is_published')
    list_filter     = ('category', 'is_published', 'start_date')
    search_fields   = ('title', 'description', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('students', 'supervisors')
    readonly_fields = ('created_at', 'updated_at')
    inlines         = [ActivityImageInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'image', 'is_published')
        }),
        ('Content', {
            'fields': ('pre_description', 'description', 'tags', 'link')
        }),
        ('Schedule & Location', {
            'fields': ('start_date', 'end_date', 'location')
        }),
        ('Participants', {
            'fields': ('students', 'supervisors'),
            'description': 'Select Students from Student table and Professors for supervisor roles.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
