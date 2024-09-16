from django.shortcuts import render, redirect
from ai_api import generate_recipes
from core.models import ExerciseRoutine, FoodRecipe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@login_required
def plate(request):
    user = request.user
    food_recipes = FoodRecipe.objects.filter(user=user)
    exercise_routines = ExerciseRoutine.objects.filter(user=user)

    if not exercise_routines.exists():
        messages.error(request, 'Primero debes generar una rutina de ejercicios.')
        return redirect('workout')

    if food_recipes.exists():
        recetas_por_dia = {}
        for recipe in food_recipes:
            dia = recipe.recipe.get('dia')
            if dia not in recetas_por_dia:
                recetas_por_dia[dia] = []
            
            # Procesar las instrucciones
            instrucciones = recipe.recipe.get('instrucciones', '')
            if isinstance(instrucciones, str):
                # Si es una cadena, dividirla en pasos
                pasos = [paso.strip() for paso in instrucciones.split('.') if paso.strip()]
            elif isinstance(instrucciones, list):
                # Si ya es una lista, usarla directamente
                pasos = instrucciones
            else:
                # Si no es ni cadena ni lista, usar una lista vacía
                pasos = []
            
            recipe_data = recipe.recipe.copy()
            recipe_data['instrucciones'] = pasos
            recetas_por_dia[dia].append(recipe_data)
        
        return render(request, 'plate.html', {'recetas_por_dia': recetas_por_dia})
    else:
        # Obtén la última rutina de ejercicios
        latest_routine = exercise_routines.latest('created_at')

        # Genera las recetas
        data = {
            'edad': user.age,
            'altura': user.height,
            'peso': user.weight,
            'ejercicio_semanal': user.weekly_exercise_hours,
            'dieta': user.diet,
            'imc': user.imc,
            'objetivo': user.goal,
            'smoker': user.smoker,
            'gym_access': user.gym_access,
            'routine': latest_routine.routine
        }
        recipes_data = generate_recipes(data)

        if 'error' in recipes_data:
            messages.error(request, recipes_data['error'])
            return redirect('workout')

        # Guarda las nuevas recetas en la base de datos
        recetas_por_dia = {}
        for recipe in recipes_data.get('plan_semanal', []):
            # Procesar las instrucciones antes de guardar
            instrucciones = recipe.get('instrucciones', '')
            if isinstance(instrucciones, str):
                pasos = [paso.strip() for paso in instrucciones.split('.') if paso.strip()]
            elif isinstance(instrucciones, list):
                pasos = instrucciones
            else:
                pasos = []
            
            recipe['instrucciones'] = pasos
            FoodRecipe.objects.create(user=user, recipe=recipe)
            
            dia = recipe.get('dia')
            if dia not in recetas_por_dia:
                recetas_por_dia[dia] = []
            recetas_por_dia[dia].append(recipe)

        messages.success(request, 'Nuevas recetas generadas exitosamente.')
        return render(request, 'plate.html', {'recetas_por_dia': recetas_por_dia})

@login_required
@csrf_exempt
def delete_recipe(request):
    if request.method == 'POST':
        user = request.user
        FoodRecipe.objects.filter(user=user).delete()
        return redirect('plate')
    return redirect('plate')