from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from .models import Recipe, Image, Ingredient, Step
from django.http import Http404, JsonResponse

class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

class OwnerRequiredMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        recipe = Recipe.objects.get(pk=pk)
        if recipe.user == request.user:
            return super().dispatch(request, pk, *args, **kwargs)
        else:
            raise Http404

class ImageOwnerRequiredMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        image = Image.objects.get(pk=pk)
        if image.recipe.user == request.user:
            return super().dispatch(request, pk, *args, **kwargs)
        else:
            raise Http404

        

# Create your views here.
class RecipeList(ListView):
    model = Recipe
    paginate_by = 6

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
        return queryset.order_by('-timestamp')



class RecipeDetail(DetailView):
    model = Recipe


class RecipeCreate(LoginRequiredMixin, CreateView):
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
        return redirect('recipe:detail',pk=obj.pk)

class RecipeUpdate(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
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
        return redirect('recipe:detail', pk=obj.pk)


class RecipeDelete(LoginRequiredMixin, OwnerRequiredMixin , DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe:list')

class ImageDelete(LoginRequiredMixin, ImageOwnerRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        image = Image.objects.get(pk=pk)
        image.delete()
        data = {
            'success':True
        }
        return JsonResponse(data)