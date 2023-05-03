from django.test import TestCase, Client
from django.urls import reverse

from to_do_list.models import Tag, Task


class TaskChangeStatusViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(content="test", deadline="2023-05-03", is_done=False)

    def test_task_is_done_toggle(self):
        url = reverse('to_do_list:task-change-is-done', args=[self.task.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_done)
        self.assertRedirects(response, reverse("to_do_list:task-list"))

    def test_task_is_done_undo_toggle(self):
        self.task.is_done = True
        self.task.save()
        url = reverse('to_do_list:task-change-is-done', args=[self.task.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_done)
        self.assertRedirects(response, reverse("to_do_list:task-list"))


class TaskCreateViewTestCase(TestCase):
    def test_task_create_view_success(self):
        data = {
            "content": "New task content",
            "deadline": "2022-01-01 12:00:00",
            "is_done": False
        }
        response = self.client.post(reverse("to_do_list:task-create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(content="New task content").exists())

    def test_task_create_view_missing_required_fields(self):
        data = {
            "content": "",
            "deadline": "2022-01-01 12:00:00",
            "is_done": False
        }
        response = self.client.post(reverse("to_do_list:task-create"), data=data)
        self.assertEqual(response.status_code,
                         200)
        self.assertFalse(Task.objects.filter(content="").exists())


class TaskUpdateViewTestCase(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            content="Test task content",
            deadline="2022-01-01 12:00:00",
            is_done=False
        )
        self.url = reverse("to_do_list:task-update", kwargs={"pk": self.task.pk})

    def test_task_update_view_success(self):
        data = {
            "content": "Updated task content",
            "deadline": "2022-01-02 12:00:00",
            "is_done": True
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.content, "Updated task content")

    def test_task_update_view_missing_required_fields(self):
        data = {
            "content": "",
            "deadline": "2022-01-01 12:00:00",
            "is_done": False
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.content, "")

