from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, Todo

from lists.views import home_page

# Create your tests here.

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data= {'item_text':'A new list item'})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST_request(self):
        response = self.client.post('/lists/new', data= {'item_text':'A new list item'})
        new_todo = Todo.objects.first()
        self.assertRedirects(response, f'/lists/{new_todo.id}/')

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        todo = Todo.objects.create()
        response = self.client.get(f'/lists/{todo.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = Todo.objects.create()
        correct_list = Todo.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertEqual(response.context['todo'], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = Todo.objects.create()
        other_list = Todo.objects.create()

        Item.objects.create(text='itemey1', todo=correct_list)
        Item.objects.create(text='itemey2', todo=correct_list)
        Item.objects.create(text='other list item 1', todo=other_list)
        Item.objects.create(text='other list item 2', todo=other_list)
        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey1')
        self.assertContains(response, 'itemey2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

class ListAndItemModelTest(TestCase):
    def test_saving_and_retreiving_items(self):
        todo = Todo()
        todo.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.todo = todo
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.todo = todo
        second_item.save()

        saved_todo = Todo.objects.first()
        self.assertEqual(saved_todo, todo)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.todo, todo)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.todo, todo)

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = Todo.objects.create()
        correct_list = Todo.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text':'A new item for an existing list'}
            )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.todo, correct_list)

    def test_redirects_to_list_view(self):
        other_list = Todo.objects.create()
        correct_list = Todo.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text':'A new item for an existing list'}
            )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
