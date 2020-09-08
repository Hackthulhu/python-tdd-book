from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, Todo

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    items = Item.objects.filter(todo=todo)
    return render(request, 'list.html', {'todo': todo})

def new_list(request):
    todo = Todo.objects.create()
    Item.objects.create(text = request.POST['item_text'], todo=todo)
    return redirect(f'/lists/{todo.id}/')

def add_item(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    Item.objects.create(text=request.POST['item_text'], todo=todo)
    return redirect(f'/lists/{todo.id}/')
