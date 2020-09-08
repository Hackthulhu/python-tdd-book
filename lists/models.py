from django.db import models

# Create your models here.
class Todo(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default='')
    todo = models.ForeignKey(Todo, default=None)
