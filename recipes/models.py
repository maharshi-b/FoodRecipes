from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, related_name='recipes',null=True)
    name = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    steps = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')

    def __str__(self):
        return self.name[:30]

