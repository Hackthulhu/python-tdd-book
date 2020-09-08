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
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        todo = Todo.objects.create()
        Item.objects.create(text='itemey1', todo=todo)
        Item.objects.create(text='itemey2', todo=todo)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey1')
        self.assertContains(response, 'itemey2')


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
