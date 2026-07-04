from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.db.models import Q
from django.utils import timezone
from .models import (
    Announcement,
    Thesis,
    Project,
    Person,
    Position,
    Topic,
    Conference,
    ResearchAnalysis,
    Publication,
    Activity,
)

def home(request):
    now = timezone.now()
    announcements = Announcement.objects.filter(
        Q(is_published=True) &
        (Q(nonstop=True) | Q(expires_at__isnull=True) | Q(expires_at__gte=now))
    ).order_by('-date')

    recent_activities = Activity.objects.filter(is_published=True).order_by('-start_date')[:5]
    for activity in recent_activities:
        activity.students_list = [f"{s.first_name} {s.last_name}" for s in activity.students.all()]
        activity.supervisors_list = [f"{p.first_name} {p.last_name}" for p in activity.supervisors.all()]
        activity.tags_list = [t.strip() for t in activity.tags.split(',') if t.strip()] if activity.tags else []

    return render(request, 'index.html', {
        'announcements': announcements,
        'recent_activities': recent_activities,
    })

def theses(request):
    ongoing = Thesis.objects.filter(
        is_published=True, status=Thesis.STATUS_ONGOING
    ).order_by('-start_date').prefetch_related('thesisparticipation_set__person', 'students', 'supervisors', 'principal_investigators')

    completed = Thesis.objects.filter(
        is_published=True, status=Thesis.STATUS_COMPLETE
    ).order_by('-end_date').prefetch_related('thesisparticipation_set__person', 'students', 'supervisors', 'principal_investigators')

    for qs in (ongoing, completed):
        for thesis in qs:
            thesis.students_list = [f"{s.first_name} {s.last_name}" for s in thesis.students.all()]
            thesis.supervisors_list = [f"{p.first_name} {p.last_name}" for p in thesis.supervisors.all()]
            thesis.pis_list = [f"{p.first_name} {p.last_name}" for p in thesis.principal_investigators.all()]
            if not thesis.slug:
                thesis.slug = slugify(thesis.title)

    return render(request, 'theses.html', {
        'ongoing_theses': ongoing,
        'completed_theses': completed,
    })

def thesis_detail(request, slug):
    thesis = get_object_or_404(Thesis, slug=slug, is_published=True)
    
    # Get students, supervisors and PIs from new M2M fields
    students = [f"{s.first_name} {s.last_name}" for s in thesis.students.all()]
    supervisors = [f"{p.first_name} {p.last_name}" for p in thesis.supervisors.all()]
    pis = [f"{p.first_name} {p.last_name}" for p in thesis.principal_investigators.all()]

    return render(request, 'thesis_detail.html', {
        'thesis': thesis,
        'students': students,
        'supervisors': supervisors,
        'pis': pis,
    })

def projects(request):
    all_projects = Project.objects.filter(
        is_published=True
    ).order_by('-start_date').prefetch_related('students', 'supervisors', 'principal_investigators')

    for project in all_projects:
        project.students_list = [f"{s.first_name} {s.last_name}" for s in project.students.all()]
        project.supervisors_list = [f"{p.first_name} {p.last_name}" for p in project.supervisors.all()]
        project.pis_list = [f"{p.first_name} {p.last_name}" for p in project.principal_investigators.all()]

    phd_projects = [p for p in all_projects if p.project_level == Project.LEVEL_PHD]
    undergrad_projects = [p for p in all_projects if p.project_level == Project.LEVEL_UNDERGRAD]

    return render(request, 'projects.html', {
        'phd_projects': phd_projects,
        'undergrad_projects': undergrad_projects,
    })

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    
    # Get students, supervisors and PIs from new M2M fields
    students = [f"{s.first_name} {s.last_name}" for s in project.students.all()]
    supervisors = [f"{p.first_name} {p.last_name}" for p in project.supervisors.all()]
    pis = [f"{p.first_name} {p.last_name}" for p in project.principal_investigators.all()]

    return render(request, 'projects_detail.html', {
        'project': project,
        'students': students,
        'supervisors': supervisors,
        'pis': pis,
    })
    
def members(request):
    from .models import Professor, Student
    
    professors = Professor.objects.filter(is_active=True).order_by('last_name', 'first_name')
    
    current_grad_students = Student.objects.filter(
        status=Student.STATUS_CURRENT,
        student_type=Student.TYPE_GRADUATE
    ).order_by('last_name', 'first_name')
    
    current_ug_students = Student.objects.filter(
        status=Student.STATUS_CURRENT,
        student_type=Student.TYPE_UNDERGRADUATE
    ).order_by('last_name', 'first_name')
    
    previous_grad_students = Student.objects.filter(
        status=Student.STATUS_PREVIOUS,
        student_type=Student.TYPE_GRADUATE
    ).order_by('last_name', 'first_name')
    
    previous_ug_students = Student.objects.filter(
        status=Student.STATUS_PREVIOUS,
        student_type=Student.TYPE_UNDERGRADUATE
    ).order_by('last_name', 'first_name')
    
    context = {
        'professors': professors,
        'current_grad_students': current_grad_students,
        'current_ug_students': current_ug_students,
        'previous_grad_students': previous_grad_students,
        'previous_ug_students': previous_ug_students,
    }
    return render(request, 'members.html', context)

def contact(request):
    from .models import Professor
    professors = Professor.objects.filter(is_active=True).order_by('last_name', 'first_name')
    return render(request, 'contact.html', {
        'professors': professors,
    })

def positions(request):
    positions = Position.objects.filter(is_published=True).order_by('order')
    ug_positions = [p for p in positions if p.position_type == Position.TYPE_UNDERGRADUATE]
    gr_positions = [p for p in positions if p.position_type == Position.TYPE_GRADUATE]
    pd_positions = [p for p in positions if p.position_type == Position.TYPE_POSTDOC]
    
    return render(request, 'positions.html', {
        'positions': positions,
        'ug_positions': ug_positions,
        'gr_positions': gr_positions,
        'pd_positions': pd_positions,
    })

def topics(request):
    topics = Topic.objects.filter(is_published=True).order_by('-start_date').prefetch_related('students', 'supervisors', 'principal_investigators')
    
    for topic in topics:
        topic.students_list = [f"{s.first_name} {s.last_name}" for s in topic.students.all()]
        topic.supervisors_list = [f"{p.first_name} {p.last_name}" for p in topic.supervisors.all()]
        topic.pis_list = [f"{p.first_name} {p.last_name}" for p in topic.principal_investigators.all()]
    
    return render(request, 'topics.html', {
        'topics': topics,
    })

def conferences(request):
    conferences = Conference.objects.filter(is_published=True).order_by('-date')
    return render(request, 'conferences.html', {
        'conferences': conferences,
    })

def research_analysis(request):
    analyses = ResearchAnalysis.objects.filter(is_published=True).prefetch_related(
        'students', 'supervisors', 'principal_investigators'
    )
    
    # Group by category
    categories = {}
    for category_code, category_name in ResearchAnalysis.CATEGORY_CHOICES:
        category_analyses = analyses.filter(category=category_code).order_by('order', 'title')
        
        # Prepare participant lists
        for analysis in category_analyses:
            analysis.students_list = [f"{s.first_name} {s.last_name}" for s in analysis.students.all()]
            analysis.supervisors_list = [f"{p.first_name} {p.last_name}" for p in analysis.supervisors.all()]
            analysis.pis_list = [f"{p.first_name} {p.last_name}" for p in analysis.principal_investigators.all()]
        
        if category_analyses.exists():
            categories[category_name] = list(category_analyses)
    
    return render(request, 'research_analysis.html', {
        'categories': categories,
    })

def research_analysis_detail(request, slug):
    analysis = get_object_or_404(ResearchAnalysis, slug=slug, is_published=True)
    
    # Get students, supervisors and PIs
    students = [f"{s.first_name} {s.last_name}" for s in analysis.students.all()]
    supervisors = [f"{p.first_name} {p.last_name}" for p in analysis.supervisors.all()]
    pis = [f"{p.first_name} {p.last_name}" for p in analysis.principal_investigators.all()]
    
    # Get related analyses from same category
    related_analyses = ResearchAnalysis.objects.filter(
        category=analysis.category,
        is_published=True
    ).exclude(pk=analysis.pk).order_by('order', 'title')[:3]
    
    # Prepare participant lists for related analyses
    for related in related_analyses:
        related.students_list = [f"{s.first_name} {s.last_name}" for s in related.students.all()]
        related.supervisors_list = [f"{p.first_name} {p.last_name}" for p in related.supervisors.all()]
        related.pis_list = [f"{p.first_name} {p.last_name}" for p in related.principal_investigators.all()]
    
    return render(request, 'research_analysis_detail.html', {
        'analysis': analysis,
        'students': students,
        'supervisors': supervisors,
        'pis': pis,
        'related_analyses': related_analyses,
    })

def publications(request):
    publications = Publication.objects.filter(is_published=True).order_by('-year', '-created_at')
    
    # Group by type
    pub_types = {}
    for type_code, type_name in Publication.TYPE_CHOICES:
        type_pubs = publications.filter(publication_type=type_code)
        if type_pubs.exists():
            pub_types[type_name] = list(type_pubs)
    
    return render(request, 'publications.html', {
        'pub_types': pub_types,
    })


def activities(request):
    activities_list = Activity.objects.filter(is_published=True).order_by('-start_date').prefetch_related('students', 'supervisors')
    
    for activity in activities_list:
        activity.students_list = [f"{s.first_name} {s.last_name}" for s in activity.students.all()]
        activity.supervisors_list = [f"{p.first_name} {p.last_name}" for p in activity.supervisors.all()]
        activity.tags_list = [t.strip() for t in activity.tags.split(',') if t.strip()] if activity.tags else []

    return render(request, 'activities.html', {
        'activities': activities_list,
    })


def activity_detail(request, slug):
    activity = get_object_or_404(Activity, slug=slug, is_published=True)
    students = [f"{s.first_name} {s.last_name}" for s in activity.students.all()]
    supervisors = [f"{p.first_name} {p.last_name}" for p in activity.supervisors.all()]
    tags = [t.strip() for t in activity.tags.split(',') if t.strip()] if activity.tags else []

    return render(request, 'activity_detail.html', {
        'activity': activity,
        'students': students,
        'supervisors': supervisors,
        'tags': tags,
    })


def announcements(request):
    announcements_list = Announcement.objects.filter(is_published=True).order_by('-date')
    return render(request, 'announcements.html', {
        'announcements': announcements_list,
    })


def announcement_detail(request, slug):
    announcement = get_object_or_404(Announcement, slug=slug, is_published=True)
    return render(request, 'announcement_detail.html', {
        'announcement': announcement,
    })
