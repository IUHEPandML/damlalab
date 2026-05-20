from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.db.models import Q
from .models import (
    Announcement,
    Thesis,
    Project,
    Person,
    Position,
    Topic,
    Conference,
)

def home(request):
    announcements = Announcement.objects.filter(is_published=True).order_by('-date')
    return render(request, 'index.html', {
        'announcements': announcements,
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
    research_projects = Project.objects.filter(
        is_published=True
    ).order_by('-start_date').prefetch_related('projectparticipation_set__person', 'students', 'supervisors', 'principal_investigators')

    for project in research_projects:
        project.students_list = [f"{s.first_name} {s.last_name}" for s in project.students.all()]
        project.supervisors_list = [f"{p.first_name} {p.last_name}" for p in project.supervisors.all()]
        project.pis_list = [f"{p.first_name} {p.last_name}" for p in project.principal_investigators.all()]

    return render(request, 'projects.html', {
        'research_projects': research_projects,
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
