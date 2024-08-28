from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import json
from ai_api import configure_api, generate_workout_routine
from django.contrib.auth.decorators import login_required

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def index(request):
    #redireccionar a workout
    return redirect('workout')

def workout(request):
    if not request.user.is_authenticated:
        return render(request, 'workout.html', {'user_authenticated': False})
    return render(request, 'workout.html', {'user_authenticated': True})


@login_required
def generate_workout(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        edad = request.POST.get('edad')
        altura = request.POST.get('altura')
        peso = request.POST.get('peso')
        ejercicio_semanal = request.POST.get('ejercicio_semanal')
        dieta = request.POST.get('dieta')
        imc = request.POST.get('imc')
        objetivo = request.POST.get('objetivo')
        fumador = request.POST.get('fumador') == 'on'  # Asegúrate de obtener el valor correctamente

        # Configura la API
        configure_api()

        # Crea un diccionario con los datos
        data = {
            'edad': edad,
            'altura': altura,
            'peso': peso,
            'ejercicio_semanal': ejercicio_semanal,
            'dieta': dieta,
            'imc': imc,
            'objetivo': objetivo,
            'smoker': fumador  # Usa 'smoker' en lugar de 'fumador'
        }

        # Genera la rutina de ejercicios
        rutina_generada = generate_workout_routine(data)

        if "error" in rutina_generada:
            # Maneja el error aquí, por ejemplo, mostrando un mensaje de error en la plantilla
            return render(request, 'error.html', {'error': rutina_generada["error"]})

        # Almacena los datos en la base de datos
        user = request.user
        user.age = edad
        user.height = altura
        user.weight = peso
        user.weekly_exercise_hours = ejercicio_semanal
        user.diet = dieta
        user.imc = imc
        user.goal = objetivo
        user.smoker = fumador
        user.save()

        rutina = {
            "usuario": {
                "edad": data['edad'],
                "altura": data['altura'],
                "peso": data['peso'],
                "ejercicio_semanal": data['ejercicio_semanal'],
                "dieta": data['dieta'],
                "imc": data['imc'],
                "objetivo": data['objetivo'],
                "fumador": data['smoker']
            },
            "rutina": rutina_generada
        }

        # Renderiza una plantilla para mostrar los datos recibidos
        return render(request, 'data_preview.html', {'data': rutina})

    return redirect('workout')