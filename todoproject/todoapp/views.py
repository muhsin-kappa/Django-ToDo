from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . forms import ToDoForms
from . models import Task

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView

# Create your views here.

class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail', kwargs={'pk': self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('home')


def home(request):
    task = Task.objects.all()
    if request.method == 'POST':
        name = request.POST.get('task', '')
        priority = request.POST.get('priority', '')
        date = request.POST.get('date', '')
        task = Task(name=name, priority=priority, date=date)
        task.save()
        return redirect('/')
    return render(request, 'home.html', {'task': task})

# def detail(request):
#
#     return render(request, 'detail.html', )

def delete(request, task_ID):
    task = Task.objects.get(id=task_ID)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'delete.html')

def update(request, task_ID):
    task = Task.objects.get(id=task_ID)
    form = ToDoForms(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'edit.html', {'form': form, 'task': task})

