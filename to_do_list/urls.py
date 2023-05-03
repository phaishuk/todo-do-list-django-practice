from django.urls import path

from to_do_list.views import (TaskListView, TaskCreateView, TaskUpdateView,
                              TaskDeleteView, TagDeleteView, TagUpdateView, TagCreateView, TaskChangeStatusView,
                              TagListView)

urlpatterns = [
    path(
        "task/<int:pk>/change-is-done/",
        TaskChangeStatusView.as_view(),
        name="task-change-is-done",
    ),
    path(
        "",
        TaskListView.as_view(),
        name="task-list",
    ),
    path(
        "task/create/",
        TaskCreateView.as_view(),
        name="task-create",
    ),
    path(
        "task/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "task/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete",
    ),
    path(
        "tag/",
        TagListView.as_view(),
        name="tag-list",
    ),
    path(
        "tag/create/",
        TagCreateView.as_view(),
        name="tag-create",
    ),
    path(
        "tag/<int:pk>/update/",
        TagUpdateView.as_view(),
        name="tag-update",
    ),
    path(
        "tag/<int:pk>/delete/",
        TagDeleteView.as_view(),
        name="tag-delete",
    ),
]

app_name = "to_do_list"
