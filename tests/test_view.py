from django.test import TestCase, Client
from django.urls import reverse

from to_do_list.models import Task, Tag


class TaskChangeStatusViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tag = Tag.objects.create(name="test_tag")
        self.task = Task.objects.create(
            content="test", deadline="2023-05-03", is_done=False
        )
        self.task.tags.add(self.tag)

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

    def setUp(self):
        self.client = Client()
        self.tag = Tag.objects.create(name="test_tag")

    def test_task_create_view_success(self):
        data = {
            "content": "New task content",
            "deadline": "2022-01-01 12:00:00",
            "is_done": False,
            "tags": [self.tag.pk]
        }
        response = self.client.post(reverse("to_do_list:task-create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(content="New task content").exists())

    def test_task_create_view_missing_required_fields(self):
        data = {
            "content": "",
            "deadline": "2022-01-01 12:00:00",
            "is_done": False,
            "tags": [self.tag.pk]
        }
        response = self.client.post(reverse("to_do_list:task-create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(content="").exists())


class TaskUpdateViewTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="test_tag")
        self.task = Task.objects.create(
            content="Test task content",
            deadline="2022-01-01 12:00:00",
            is_done=False
        )
        self.task.tags.add(self.tag)
        self.url = reverse("to_do_list:task-update", kwargs={"pk": self.task.pk})

    def test_task_update_view_success(self):
        data = {
            "content": "Updated task content",
            "deadline": "2022-01-02 12:00:00",
            "is_done": True,
            "tags": [self.tag.pk],
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.content, "Updated task content")

    def test_task_update_view_missing_required_fields(self):
        data = {
            "content": "",
            "deadline": "2022-01-01 12:00:00",
            "is_done": False,
            "tags": [self.tag.pk],
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.content, "")


class TagCreateViewTestCase(TestCase):

    def test_tag_create_view_success(self):
        response = self.client.post(reverse("to_do_list:tag-create"), data={"name": "test_tag"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tag.objects.filter(name="test_tag").exists())

    def test_tag_create_view_missing_required_fields(self):
        response = self.client.post(reverse("to_do_list:tag-create"), data={})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tag.objects.filter(name="").exists())


class TagUpdateViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.tag = Tag.objects.create(name="test_tag")
        self.url = reverse("to_do_list:tag-update", kwargs={"pk": self.tag.pk})

    def test_task_update_view_success(self):
        response = self.client.post(self.url, data={"name": "test_tag2"})
        self.assertEqual(response.status_code, 302)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "test_tag2")

    def test_task_update_view_missing_required_fields(self):
        response = self.client.post(self.url, data={"name": ""})
        self.assertEqual(response.status_code, 200)
        self.tag.refresh_from_db()
        self.assertNotEqual(self.tag.name, "")


class TaskListViewTestCase(TestCase):

    def test_task_list_view(self):
        response = self.client.get(reverse("to_do_list:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "to_do_list/task_list.html")


class TagListViewTestCase(TestCase):

    def test_tag_list_view(self):
        response = self.client.get(reverse("to_do_list:tag-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "to_do_list/tag_list.html")
