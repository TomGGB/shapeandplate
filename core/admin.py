from django.contrib import admin

# Register your models here.

from .models import User, ExerciseRoutine, FoodRecipe

admin.site.register(User)
admin.site.register(ExerciseRoutine)
admin.site.register(FoodRecipe)