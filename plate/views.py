from django.shortcuts import render, redirect
from ai_api import generate_recipes
from core.models import ExerciseRoutine, FoodRecipe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from .forms import AllergyForm
from django.utils import timezone

@login_required
def plate(request):
    user = request.user
    food_recipes = FoodRecipe.objects.filter(user=user)
    exercise_routines = ExerciseRoutine.objects.filter(user=user)
    if not exercise_routines.exists():
        messages.error(request, 'Primero debes generar una rutina de ejercicios.')
        return redirect('workout')

    # Manejo del formulario de alergias
    if request.method == 'POST':
        form = AllergyForm(request.POST)
        if form.is_valid():
            allergies = form.cleaned_data['allergies']
            # Guarda las alergias en el perfil del usuario
            user.allergies = allergies
            user.save()
            messages.success(request, '¡Alergias actualizadas correctamente! La próxima vez que se generen recetas se tendrán en consideración.')
            return redirect('plate')
    else:
        # Inicializa el formulario con las alergias actuales del usuario
        form = AllergyForm(initial={'allergies': user.allergies})

    # Definir los días de la semana
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    # Obtener el día actual
    today = timezone.now()
    start_of_week = today - timedelta(days=today.weekday())
    week_days = [(start_of_week + timedelta(days=i)).strftime('%d') for i in range(7)]
    # Combinar días de la semana y números de días
    week_info = list(zip(dias_semana, week_days))
    # Obtener el día seleccionado o el día actual
    selected_day = request.GET.get('day')
    if selected_day:
        dia_actual = selected_day
    else:
        dia_actual = dias_semana[today.weekday()]

    recetas_del_dia = {}
    if food_recipes.exists():
        for recipe in food_recipes:
            if recipe.recipe.get('dia') == dia_actual:
                tipo = recipe.recipe.get('tipo')
                if tipo not in recetas_del_dia:
                    recetas_del_dia[tipo] = []
                recipe_data = recipe.recipe.copy()
                recipe_data['id'] = recipe.id
                recetas_del_dia[tipo].append(recipe_data)
    else:
        # Generar nuevas recetas si no existen
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
            'allergies': user.allergies.split(',') if user.allergies else []
        }
        new_recipes = generate_recipes(data)
        if 'plan_semanal' in new_recipes:
            for recipe in new_recipes['plan_semanal']:
                FoodRecipe.objects.create(user=user, recipe=recipe)
            messages.success(request, 'Nuevas recetas generadas exitosamente.')
            return redirect('plate')
        else:
            messages.error(request, 'No se pudieron generar nuevas recetas. Por favor, intenta de nuevo.')

    return render(request, 'plate.html', {
        'recetas_del_dia': recetas_del_dia,
        'dia_actual': dia_actual,
        'week_info': week_info,
        'form': form,  # Añade el formulario al contexto
    })

@login_required
@csrf_exempt
def delete_recipe(request):
    user = request.user
    messages.success(request, 'Todas las recetas han sido eliminadas. Se generarán nuevas recetas.')
    FoodRecipe.objects.filter(user=user).delete()
    return redirect('plate')

@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(FoodRecipe, id=recipe_id, user=request.user)
    instrucciones = recipe.recipe.get('instrucciones', '').split('. ')
    return render(request, 'recipe_detail.html', {'receta': recipe.recipe, 'instrucciones': instrucciones})
