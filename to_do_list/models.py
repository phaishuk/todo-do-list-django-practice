from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):

    class Meta:
        ordering = ["is_done"]

    content = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    is_done = models.BooleanField()
    tags = models.ManyToManyField(to=Tag, related_name="tasks")

    def __str__(self):
        return self.content
