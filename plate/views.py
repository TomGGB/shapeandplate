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
    else:
        latest_routine = exercise_routines.latest('created_at')

    # Generar recetas si no existen
    if not food_recipes.exists():
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
            'allergies': user.allergies if user.allergies else '', 
            'routine': latest_routine.routine,
        }
        recipes_data = generate_recipes(data)

        if 'error' in recipes_data:
            messages.error(request, 'Hubo un error al generar las recetas. Por favor, intenta de nuevo.')
            return redirect('workout')
        else:
            # Guarda el JSON completo
            FoodRecipe.objects.create(user=user, plan_semanal=recipes_data)
            # Actualizar la variable food_recipes
            food_recipes = FoodRecipe.objects.filter(user=user)

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

    # Inicializar el diccionario para todas las recetas de la semana
    recetas_semana = {dia: {} for dia in dias_semana}

    if food_recipes.exists():
        # Obtener el plan_semanal más reciente
        latest_food_recipe = food_recipes.latest('created_at')
        plan_semanal = latest_food_recipe.plan_semanal.get('plan_semanal', [])

        for idx, receta in enumerate(plan_semanal):
            receta['id'] = idx  # Asignar un identificador único
            dia = receta.get('dia')
            tipo = receta.get('tipo')
            if dia in recetas_semana:
                if tipo not in recetas_semana[dia]:
                    recetas_semana[dia][tipo] = []
                recetas_semana[dia][tipo].append(receta)

    # Obtener el día seleccionado o el día actual
    selected_day = request.GET.get('day')
    if selected_day:
        dia_actual = selected_day
    else:
        dia_actual = dias_semana[today.weekday()]

    recetas_del_dia = recetas_semana.get(dia_actual, {})

    # Pasar 'recetas_del_dia' al contexto
    context = {
        'recetas_del_dia': recetas_del_dia,
        'dia_actual': dia_actual,
        'week_info': week_info,
        'form': form,
    }
    return render(request, 'plate.html', context)

@login_required
@csrf_exempt
def delete_recipe(request):
    user = request.user
    messages.success(request, 'Todas las recetas han sido eliminadas. Se generarán nuevas recetas.')
    FoodRecipe.objects.filter(user=user).delete()
    return redirect('plate')

@login_required
def recipe_detail(request, recipe_idx):
    food_recipe = FoodRecipe.objects.filter(user=request.user).latest('created_at')
    plan_semanal = food_recipe.plan_semanal.get('plan_semanal', [])
    if recipe_idx < 0 or recipe_idx >= len(plan_semanal):
        messages.error(request, 'Receta no encontrada.')
        return redirect('plate')
    receta = plan_semanal[recipe_idx]
    instrucciones = receta.get('instrucciones', [])
    return render(request, 'recipe_detail.html', {'receta': receta, 'instrucciones': instrucciones})
