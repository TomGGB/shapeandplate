from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import json
from ai_api import configure_api, generate_workout_routine

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def index(request):
    #redireccionar a workout
    return redirect('workout')

def workout(request):
    return render(request, 'workout.html')

def generate_workout(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        edad = request.POST.get('edad')
        altura = request.POST.get('altura')
        peso = request.POST.get('peso')
        ejercicio_semanal = request.POST.get('ejercicio_semanal')
        dieta = request.POST.get('dieta')

        # Configura la API
        configure_api()

        # Crea un diccionario con los datos
        data = {
            'edad': edad,
            'altura': altura,
            'peso': peso,
            'ejercicio_semanal': ejercicio_semanal,
            'dieta': dieta
        }

        # Genera la rutina de ejercicios
        rutina_generada = generate_workout_routine(data)

        rutina = {
            "usuario": {
                "edad": data['edad'],
                "altura": data['altura'],
                "peso": data['peso'],
                "ejercicio_semanal": data['ejercicio_semanal'],
                "dieta": data['dieta']
            },
            "rutina": rutina_generada
        }

        # Renderiza una plantilla para mostrar los datos recibidos
        return render(request, 'data_preview.html', {'data': rutina})

    return redirect('workout')