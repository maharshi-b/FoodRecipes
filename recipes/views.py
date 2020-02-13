from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe

# Create your views here.
class RecipeList(ListView):
    model = Recipe
    paginate_by = 6

class RecipeDetail(DetailView):
    model = Recipe