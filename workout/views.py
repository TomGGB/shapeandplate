from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import uuid
import json
import google.generativeai as genai
from .models import Usuario

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def workout(request):
    return render(request, 'workout.html')


def generate_workout(request):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
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
    system_instruction="Eres un personal trainer, se ingresarán los datos del usuario y debes darle una rutina personalizada con el nombre del ejercicio(nombre), duración(duracion), repeticiones(rep), sesiones(sesiones), intensidad(i) y la descipcion de cada ejercicio(desc)\ntambien debes retornar la url de una imagen descriptiva de cada ejercicio sacada de internet",
    )

    user = Usuario()