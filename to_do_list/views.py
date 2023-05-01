from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from to_do_list.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task


class TaskChangeStatusView(generic.View):

    @staticmethod
    def get(request, pk):
        task = get_object_or_404(Task, id=pk)
        task.is_done = not task.is_done
        task.save()

        return redirect(request.META.get("HTTP_REFERER"))


class TaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("to_do_list:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("to_do_list:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task


class TagListView(generic.ListView):
    model = Tag


class TagCreateView(generic.CreateView):
    model = Tag


class TagUpdateView(generic.UpdateView):
    model = Tag


class TagDeleteView(generic.DeleteView):
    model = Task

