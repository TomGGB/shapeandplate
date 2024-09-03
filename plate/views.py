from django.shortcuts import render, redirect
from ai_api import generate_recipes
from core.models import ExerciseRoutine, FoodRecipe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def plate(request):
    user = request.user
    exercise_routines = ExerciseRoutine.objects.filter(user=user)
    recipes = FoodRecipe.objects.filter(user=user)
    if recipes.exists():
        # Convertir las recetas a la nueva estructura
        recetas = []
        for recipe in recipes:
            for receta in recipe.recipe['recetas']:
                if isinstance(receta['instrucciones'], str):
                    receta['instrucciones'] = receta['instrucciones'].split('. ')
                recetas.append(receta)
        return render(request, 'plate.html', {'recetas': recetas})
    else:
        data = {
            "edad": user.age,
            "altura": user.height,
            "peso": user.weight,
            "ejercicio_semanal": user.weekly_exercise_hours,
            "dieta": user.diet,
            "imc": user.imc,
            "objetivo": user.goal,
            "smoker": user.smoker,
            "gym_access": user.gym_access,
            "routine": exercise_routines.first().routine
        }

        recipe_data = generate_recipes(data)
        recipe = FoodRecipe.objects.create(user=user, recipe=recipe_data)
        recipe.save()

        # Convertir la receta generada a la nueva estructura
        recetas = []
        for receta in recipe.recipe['recetas']:
            if isinstance(receta['instrucciones'], str):
                receta['instrucciones'] = receta['instrucciones'].split('. ')
            recetas.append(receta)

        return render(request, 'plate.html', {'recetas': recetas})

@login_required
@csrf_exempt
def delete_recipe(request):
    if request.method == 'POST':
        user = request.user
        FoodRecipe.objects.filter(user=user).delete()
        return redirect('plate')
    return render(request, 'plate.html')