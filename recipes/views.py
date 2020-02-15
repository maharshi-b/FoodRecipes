from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from .models import Recipe, Image, Ingredient
from .forms import RecipeForm, ImageForm

# Create your views here.
class RecipeList(ListView):
    model = Recipe
    paginate_by = 6
    ordering = ['timestamp']

class RecipeDetail(DetailView):
    model = Recipe


class RecipeCreate(View):
    def get(self, request, *args, **kwargs):
        context = {
            'recipe_form':RecipeForm(),
            'image_form':ImageForm()
        }
        return render(request, 'recipes/recipe_form.html', context)

    def post(self, request, *args, **kwargs):
        recipe_form = RecipeForm(request.POST)
        if recipe_form.is_valid():
            obj = recipe_form.save(commit=False)
            obj.user = request.user
            obj.save()
            ings = request.POST.get('ingredients')
            ings = ings.split(',')
            for ing in ings:
                print('kkkk' + ing)
                i,_=Ingredient.objects.get_or_create(name=ing)
                obj.ingredients.add(i)
            obj.save()
            for img in request.FILES.getlist('image'):
                img_obj = Image.objects.create(image=img, recipe=obj)
            return redirect("recipe:list")
        context = {
            'recipe_form':recipe_form,
            'image_form':image_form
        }
        return render(request, 'recipes/recipe_form.html', context)


