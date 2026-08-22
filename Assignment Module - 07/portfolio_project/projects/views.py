from django.shortcuts import render, get_object_or_404
from .models import Project

# Create your views here.

def home(request):
    return render(request, 'projects/home.html')

def about(request):
    return render(request, 'projects/about.html')

def projects_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects/projects.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})