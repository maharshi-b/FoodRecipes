from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView
from .models import Recipe, Image, Ingredient, Step

# Create your views here.
class RecipeList(ListView):
    model = Recipe
    paginate_by = 2

    def get_queryset(self):
        queryset = super(RecipeList, self).get_queryset()
        q = self.request.GET.get('q',None)
        if q is not None:
            queryset = queryset.filter(name__icontains=q)
            ing = Ingredient.objects.filter(name=q)
            if ing.exists():
                qs2 = ing.first().recipes.all()
                queryset = queryset.union(qs2)
        u = self.request.GET.get('u', None)
        if u is not None:
            queryset = queryset.filter(user=self.request.user)
        return queryset



class RecipeDetail(DetailView):
    model = Recipe


class RecipeCreate(CreateView):
    model = Recipe
    fields = ['name','description']
    template_name = 'recipes/recipe_form.html'
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        for ing in self.request.POST.get('ingredients').split(','):
            i,_=Ingredient.objects.get_or_create(name=ing)
            obj.ingredients.add(i)
        for img in self.request.FILES.getlist('image'):
            img = Image.objects.create(image=img, recipe=obj)
        i = 1
        while(True):
            name = 'steps_' + str(i)
            if name in self.request.POST:
                Step.objects.create(description=self.request.POST.get(name), recipe=obj)
                i = i + 1
            else:
                break
        return redirect('recipe:list')

class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['name','description']
    template_name = 'recipes/recipe_update_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        obj.ingredients.clear()
        obj.step_set.all().delete()
        obj.save()
        for ing in self.request.POST.get('ingredients').split(','):
            i,_=Ingredient.objects.get_or_create(name=ing)
            obj.ingredients.add(i)
        for img in self.request.FILES.getlist('image'):
            img = Image.objects.create(image=img, recipe=obj)
        i = 1
        while(True):
            name = 'steps_' + str(i)
            if name in self.request.POST:
                Step.objects.create(description=self.request.POST.get(name), recipe=obj)
                i = i + 1
            else:
                break
        return redirect('recipe:list')
