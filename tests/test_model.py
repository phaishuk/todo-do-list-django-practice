from datetime import datetime

from django.db import IntegrityError, models
from django.test import TestCase

from to_do_list.models import Tag, Task


class TagModelTestPublic(TestCase):
    def test_tag_creation(self):
        name = "Test tag"
        tag = Tag.objects.create(name=name)

        self.assertEqual(tag.name, name)
        self.assertIsNotNone(tag.id)

    def test_tag_string_representation(self):
        name = "Test tag"
        tag = Tag.objects.create(name=name)
        tag_str = str(tag)

        self.assertEqual(tag_str, name)

    def test_tag_uniqueness(self):
        name = "Test tag"
        Tag.objects.create(name=name)

        with self.assertRaises(IntegrityError):
            Tag.objects.create(name=name)

    def test_field_params(self):
        self.assertEqual(Tag._meta.get_field("name").max_length, 255)


class TaskModelTestCase(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name="test_tag")

    def test_create_task(self):
        task = Task.objects.create(
            content="test_content",
            deadline="2023-05-03 23:59:59",
            is_done=False,
        )
        task.tags.add(self.tag)
        self.assertEqual(task.content, "test_content")
        self.assertEqual(task.is_done, False)
        self.assertEqual(task.tags.count(), 1)
        self.assertEqual(str(task), "test_content")

    def test_field_params(self):
        self.assertEqual(Task._meta.get_field("content").max_length, 255)
        self.assertEqual(Task._meta.get_field("tags").related_model, Tag)
        self.assertEqual(Task._meta.ordering, ["is_done"])

    def test_add_tag_to_task(self):
        task = Task.objects.create(
            content="test_content",
            deadline="2023-05-03 23:59:59",
            is_done=False,
        )
        tag = Tag.objects.create(name="test_tag2")
        task.tags.add(tag)
        self.assertEqual(task.tags.count(), 1)
        self.assertEqual(task.tags.first(), tag)

    def test_task_ordering(self):
        ordering = Task._meta.ordering
        self.assertEqual(ordering, ['is_done'])

    def test_tags_field(self):
        field = Task._meta.get_field('tags')
        self.assertIsInstance(field, models.ManyToManyField)
        self.assertEqual(field.related_model, Tag)
        self.assertEqual(field._related_name, 'tasks')

    def test_task_tag_relationship(self):
        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2')
        task1 = Task.objects.create(content='content1', deadline=datetime.now(), is_done=False)
        task2 = Task.objects.create(content='content2', deadline=datetime.now(), is_done=False)
        task1.tags.add(tag1)
        task1.tags.add(tag2)
        task2.tags.add(tag2)
        self.assertIn(task1, tag1.tasks.all())
        self.assertIn(task1, tag2.tasks.all())
        self.assertIn(task2, tag2.tasks.all())
        self.assertNotIn(task2, tag1.tasks.all())

    def test_task_model_str_method(self):
        task = Task.objects.create(content="Test Task", deadline=datetime.now(), is_done=False)
        self.assertEqual(str(task), "Test Task")
