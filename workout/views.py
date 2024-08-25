from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai

# Carga las variables de entorno desde el archivo .env
load_dotenv()

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

        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="Eres un personal trainer, se ingresarán los datos del usuario y debes darle una rutina personalizada con el nombre del ejercicio(nombre), duración(duracion), repeticiones(rep), sesiones(sesiones), intensidad(i) y la descipcion de cada ejercicio(desc)",
        )

        chat_session = model.start_chat(
            history=[]
        )
        # Crea un diccionario con los datos
        data = {
            'edad': edad,
            'altura': altura,
            'peso': peso,
            'ejercicio_semanal': ejercicio_semanal,
            'dieta': dieta
        }

        mensaje = f'Datos del usuario: \nEdad: {edad} \nAltura: {altura} \nPeso: {peso} \nEjercicio semanal: {ejercicio_semanal} \nDieta: {dieta}'
        response = chat_session.send_message(mensaje)
        
        rutina = {
            "usuario": {
                "edad": data['edad'],
                "altura": data['altura'],
                "peso": data['peso'],
                "ejercicio_semanal": data['ejercicio_semanal'],
                "dieta": data['dieta']
            },
            "rutina": json.loads(response.text)
        }

        # Renderiza una plantilla para mostrar los datos recibidos
        return render(request, 'data_preview.html', {'data': rutina})

    return redirect('workout')