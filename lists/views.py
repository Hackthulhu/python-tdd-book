from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, Todo

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    todo = Todo.objects.create()
    Item.objects.create(text = request.POST['item_text'], todo=todo)
    return redirect('/lists/the-only-list-in-the-world/')
