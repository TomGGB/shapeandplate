from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import json
from ai_api import configure_api, generate_workout_routine
from django.contrib.auth.decorators import login_required
from core.models import ExerciseRoutine, FoodRecipe
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def index(request):
    # Redireccionar a workout
    return redirect('workout')

@login_required
def workout(request):
    user = request.user
    exercise_routines = ExerciseRoutine.objects.filter(user=user)

    context = {
        'user_authenticated': True,
        'routine': exercise_routines.first() if exercise_routines.exists() else None,
        'user': user
    }

    if exercise_routines.exists():
        return redirect('data_preview')
    else:
        return render(request, 'workout.html', context)

@login_required
def generate_workout(request):
    if request.method == 'POST':
        user = request.user

        # Obtén los datos del formulario
        user.age = request.POST.get('edad', user.age)
        user.height = request.POST.get('altura', user.height)
        user.weight = request.POST.get('peso', user.weight)
        user.weekly_exercise_hours = request.POST.get('ejercicio_semanal', user.weekly_exercise_hours)
        user.diet = request.POST.get('dieta', user.diet)
        
        imc = request.POST.get('imc', user.imc)
        if imc:
            imc = imc.replace(',', '.')  # Reemplaza la coma por un punto
            user.imc = float(imc)  # Convierte la cadena a un número
        
        user.goal = request.POST.get('goal', user.goal)
        user.smoker = 'smoker' in request.POST
        user.gym_access = 'gym_access' in request.POST

        # Guarda los datos del usuario
        user.save()

        # Genera la rutina de ejercicios
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
            'allergies': user.allergies,
            'gender': user.gender  # Añadir el campo de género
        }
        routine_data = generate_workout_routine(data)
        
        # Verificar si hay error antes de guardar
        if isinstance(routine_data, dict) and 'error' in routine_data:
            messages.error(request, routine_data['error'])
            return redirect('workout')

        # Verificar que tenga la estructura correcta
        if not isinstance(routine_data, dict) or 'rutina' not in routine_data:
            messages.error(request, 'La rutina generada no tiene el formato correcto.')
            return redirect('workout')

        # Si todo está bien, guardar la rutina
        routine = ExerciseRoutine.objects.create(user=user, routine=routine_data)
        routine.save()
        
        messages.success(request, 'Nueva rutina de ejercicios generada exitosamente.')
        return redirect('data_preview')

    return redirect('workout')

@login_required
def data_preview(request):
    user = request.user
    exercise_routines = ExerciseRoutine.objects.filter(user=user)

    if not exercise_routines.exists():
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
            'gender': user.gender
        }
        
        routine_data = generate_workout_routine(data)
        
        # Verificar si hay error o formato incorrecto
        if isinstance(routine_data, dict) and ('error' in routine_data or 'rutina' not in routine_data):
            messages.error(request, 'No se pudo generar la rutina de ejercicios. Por favor, intenta de nuevo.')
            return redirect('workout')
            
        # Si todo está bien, guardar la rutina
        routine = ExerciseRoutine.objects.create(user=user, routine=routine_data)
        return render(request, 'data_preview.html', {'exercise_routine': routine_data})

    if exercise_routines.exists():
        latest_routine = exercise_routines.latest('created_at')
        routine_data = latest_routine.routine
        progress_data = latest_routine.progress
        exercise_times = latest_routine.exercise_times



        if request.method == 'POST':
            exercise_index = int(request.POST.get('exercise_index'))
            completed = request.POST.get('completed') == 'true'
            time_spent = int(request.POST.get('time_spent', 0))
            
            # Inicializa el progreso si no existe
            if str(exercise_index) not in progress_data:
                progress_data[str(exercise_index)] = {'completed': False, 'count': 0}
            
            # Actualiza el progreso
            if completed:
                progress_data[str(exercise_index)]['completed'] = True
                progress_data[str(exercise_index)]['count'] += 1
            
            # Registra el tiempo de ejercicio
            if str(exercise_index) not in exercise_times:
                exercise_times[str(exercise_index)] = []
            exercise_times[str(exercise_index)].append(time_spent)

            # Guarda los cambios en la base de datos
            latest_routine.progress = progress_data
            latest_routine.exercise_times = exercise_times
            latest_routine.save()
        # Actualiza los datos de la rutina con el progreso
        for i, exercise in enumerate(routine_data['rutina']):
            exercise['progress'] = progress_data.get(str(i), {'completed': False, 'count': 0})
            exercise['times'] = exercise_times.get(str(i), [])

        return render(request, 'data_preview.html', {'exercise_routine': routine_data})
    else:
        # Genera una nueva rutina si no existe
        data = {
            'edad': user.age,
            'altura': user.height,
            'peso': user.weight,
            'ejercicio_semanal': user.weekly_exercise_hours,
            'dieta': user.diet,
            'imc': user.imc,
            'objetivo': user.goal,
            'smoker': user.smoker,
            'gym_access': user.gym_access
        }
        routine_data = generate_workout_routine(data)
        if 'error' in routine_data:
            messages.error(request, 'No se pudo generar la rutina de ejercicios. Por favor, intenta de nuevo.')
            return redirect('workout')

        else:
            # Guarda la nueva rutina en la base de datos
            routine = ExerciseRoutine.objects.create(user=user, routine=routine_data)
            routine.save()

            return render(request, 'data_preview.html', {'exercise_routine': routine_data})

        
    
@csrf_exempt
@login_required
def delete_routine(request):
    if request.method == 'POST':
        user = request.user
        ExerciseRoutine.objects.filter(user=user).delete()
        FoodRecipe.objects.filter(user=user).delete()
        return redirect('workout')
    return redirect('workout')