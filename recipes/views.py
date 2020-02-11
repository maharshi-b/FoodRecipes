from django.shortcuts import render
from django.views.generic import ListView
from .models import Recipe

# Create your views here.
class RecipeList(ListView):
    model = Recipe
    paginate_by = 2