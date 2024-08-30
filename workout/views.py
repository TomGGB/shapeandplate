from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import json
from ai_api import configure_api, generate_workout_routine
from django.contrib.auth.decorators import login_required
from core.models import ExerciseRoutine
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
            'smoker': user.smoker
        }
        routine_data = generate_workout_routine(data)

        # Guarda la rutina en la base de datos
        routine = ExerciseRoutine.objects.create(user=user, routine=routine_data)
        routine.save()

        messages.success(request, 'Datos guardados y rutina generada correctamente.')
        return redirect('data_preview')

@login_required
def data_preview(request):
    user = request.user
    exercise_routines = ExerciseRoutine.objects.filter(user=user)

    if exercise_routines.exists():
        return render(request, 'data_preview.html', {'exercise_routines': exercise_routines})
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
            'smoker': user.smoker
        }
        routine_data = generate_workout_routine(data)

        # Guarda la nueva rutina en la base de datos
        routine = ExerciseRoutine.objects.create(user=user, routine=routine_data)
        routine.save()

        return render(request, 'data_preview.html', {'exercise_routines': [routine]})

@csrf_exempt
@login_required
def delete_routine(request):
    if request.method == 'POST':
        user = request.user
        ExerciseRoutine.objects.filter(user=user).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)