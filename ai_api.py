import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def configure_api():
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)

def generate_workout_routine(data):
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

    mensaje = f'Datos del usuario: \nEdad: {data["edad"]} \nAltura: {data["altura"]} \nPeso: {data["peso"]} \nEjercicio semanal: {data["ejercicio_semanal"]} \nDieta: {data["dieta"]}'
    response = chat_session.send_message(mensaje)
    
    return json.loads(response.text)