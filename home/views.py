from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import FoodRecipe, ExerciseRoutine
from datetime import datetime
import pytz

# Create your views here.

@login_required
def index(request):
    # Obtener la hora actual en Chile
    chile_tz = pytz.timezone('America/Santiago')
    current_time = datetime.now(chile_tz)
    hour = current_time.hour

    # Determinar el tipo de comida según la hora
    if 6 <= hour < 10:
        current_meal_type = "Desayuno"
    elif 10 <= hour < 12:
        current_meal_type = "Colación"
    elif 12 <= hour < 15:
        current_meal_type = "Almuerzo"
    elif 15 <= hour < 18:
        current_meal_type = "Colación"
    elif 18 <= hour < 22:
        current_meal_type = "Cena"
    else:
        current_meal_type = None

    # Obtener el día actual
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    dia_actual = dias_semana[current_time.weekday()]

    # Obtener la receta actual
    current_meal = None
    if current_meal_type:
        recipes = FoodRecipe.objects.filter(user=request.user)
        for recipe in recipes:
            if recipe.recipe.get('dia') == dia_actual and recipe.recipe.get('tipo') == current_meal_type:
                recipe_data = recipe.recipe
                recipe_data['id'] = recipe.id
                current_meal = recipe_data
                break

    # Obtener ejercicios pendientes y métricas
    exercise_routine = ExerciseRoutine.objects.filter(user=request.user).first()
    today_exercises = []
    completed_count = 0
    total_exercises = 0

    if exercise_routine:
        routine_data = exercise_routine.routine
        progress_data = exercise_routine.progress or {}

        for i, exercise in enumerate(routine_data.get('rutina', [])):
            # Excluir ejercicios que contengan 'calentamiento' o 'enfriamiento' en su nombre
            nombre_ejercicio = exercise.get('nombre', '').lower()
            if 'calentamiento' not in nombre_ejercicio and 'enfriamiento' not in nombre_ejercicio:
                total_exercises += 1
                exercise_progress = progress_data.get(str(i), {})
                exercise['completed'] = exercise_progress.get('completed', False)
                
                if exercise['completed']:
                    completed_count += 1
                else:
                    today_exercises.append(exercise)

    completion_percentage = (completed_count / total_exercises * 100) if total_exercises > 0 else 0

    context = {
        'current_meal': current_meal,
        'current_meal_type': current_meal_type,
        'today_exercises': today_exercises[:3],
        'completion_percentage': round(completion_percentage, 1),
        'completed_count': completed_count,
        'total_exercises': total_exercises
    }

    return render(request, 'home.html', context)
