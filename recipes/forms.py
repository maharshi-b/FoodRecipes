from django import forms
from .models import Recipe, Image, Step


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'description']
    

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image']
