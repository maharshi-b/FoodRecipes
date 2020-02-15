from django.contrib import admin
from .models import Recipe, Ingredient, Image, Step
# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Image)
admin.site.register(Step)