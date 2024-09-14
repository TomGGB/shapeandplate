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
        # Convertir las recetas a la nueva estructura y agrupar por días
        recetas_por_dia = {}
        for recipe in recipes:
            for receta in recipe.recipe['recetas']:
                if isinstance(receta['instrucciones'], str):
                    receta['instrucciones'] = receta['instrucciones'].split('. ')
                dia = receta.get('dia', '1')  # Asume que cada receta tiene un campo 'dia'
                if dia not in recetas_por_dia:
                    recetas_por_dia[dia] = []
                recetas_por_dia[dia].append(receta)
        return render(request, 'plate.html', {'recetas_por_dia': recetas_por_dia})
    else:
        routine = exercise_routines.first()
        if not routine:
            return render(request, 'plate.html', {'no_routines_message': 'Para obtener recetas personalizadas, por favor genera una nueva rutina de ejercicios.'})
        
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
            "routine": routine.routine
        }

        previous_recipes = [recipe.recipe for recipe in recipes] if recipes.exists() else None
        recipe_data = generate_recipes(data, previous_recipes)
        recipe = FoodRecipe.objects.create(user=user, recipe=recipe_data)
        recipe.save()

        # Convertir la receta generada a la nueva estructura y agrupar por días
        recetas_por_dia = {}
        for receta in recipe.recipe['recetas']:
            if isinstance(receta['instrucciones'], str):
                receta['instrucciones'] = receta['instrucciones'].split('. ')
            dia = receta.get('dia', '1')  # Asume que cada receta tiene un campo 'dia'
            if dia not in recetas_por_dia:
                recetas_por_dia[dia] = []
            recetas_por_dia[dia].append(receta)

        return render(request, 'plate.html', {'recetas_por_dia': recetas_por_dia})

@login_required
@csrf_exempt
def delete_recipe(request):
    if request.method == 'POST':
        user = request.user
        previous_recipes = FoodRecipe.objects.filter(user=user)
        
        # Convertir el QuerySet a una lista de diccionarios
        previous_recipes_list = list(previous_recipes.values())
        
        FoodRecipe.objects.filter(user=user).delete()
        request.session['previous_recipes'] = previous_recipes_list
        return redirect('plate')
    return render(request, 'plate.html')