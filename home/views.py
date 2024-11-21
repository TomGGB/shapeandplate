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
    current_meal_type = None
    current_meal = None
    all_exercises = []

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
        if recipes.exists():
            latest_recipe = recipes.latest('created_at')
            plan_semanal = latest_recipe.plan_semanal.get('plan_semanal', [])
            
            for recipe in plan_semanal:
                if recipe.get('dia') == dia_actual and recipe.get('tipo') == current_meal_type:
                    recipe['id'] = recipe.get('id', 0)  # Asignar ID si no existe
                    current_meal = recipe
                    break

    # Obtener ejercicios pendientes y métricas
    exercise_routine = ExerciseRoutine.objects.filter(user=request.user).first()
    today_exercises = []
    completed_count = 0
    total_exercises = 0

    if exercise_routine and exercise_routine.routine:
        routine_data = exercise_routine.routine
        progress_data = exercise_routine.progress or {}
        all_exercises = []

        for i, exercise in enumerate(routine_data.get('rutina', [])):
            nombre_ejercicio = exercise.get('nombre', '').lower()
            if 'calentamiento' not in nombre_ejercicio and 'enfriamiento' not in nombre_ejercicio:
                exercise_progress = progress_data.get(str(i), {})
                exercise['completed'] = exercise_progress.get('completed', False)
                all_exercises.append(exercise)
                
                if exercise['completed']:
                    completed_count += 1
                else:
                    today_exercises.append(exercise)
                total_exercises += 1

    completion_percentage = (completed_count / len(all_exercises) * 100) if all_exercises else 0

    # Verificar si hay rutinas y recetas
    has_routine = ExerciseRoutine.objects.filter(user=request.user).exists()
    has_recipes = FoodRecipe.objects.filter(user=request.user).exists()

    context = {
        'current_meal': current_meal,
        'current_meal_type': current_meal_type,
        'today_exercises': today_exercises,
        'completion_percentage': round(completion_percentage, 1),
        'completed_count': completed_count,
        'total_exercises': len(all_exercises) if all_exercises else 0,
        'has_routine': has_routine,
        'has_recipes': has_recipes
    }

    return render(request, 'home.html', context)
