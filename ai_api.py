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
        system_instruction="Eres un personal trainer, se ingresarán los datos del usuario y debes darle una rutina personalizada con el nombre del ejercicio(nombre), duración(duracion), repeticiones(rep), sesiones(sesiones), intensidad(i), puede ser 'Baja', 'Media' o 'Alta' y la descipcion de cada ejercicio(desc)",
    )

    chat_session = model.start_chat(
        history=[]
    )

    mensaje = (
        f'Datos del usuario: \n'
        f'Edad: {data["edad"]} \n'
        f'Altura: {data["altura"]} \n'
        f'Peso: {data["peso"]} \n'
        f'Horas de ejercicio que hace en la semana: {data["ejercicio_semanal"]} \n'
        f'Dieta: {data["dieta"]} \n'
        f'Indice de masa corporal: {data["imc"]} \n'
        f'Objetivo: {data["objetivo"]} \n'
        f'Fumador: {"Sí" if data["smoker"] else "No"}'
    )
    
    try:
        response = chat_session.send_message(mensaje)
        return json.loads(response.text)
    except genai.generation_types.StopCandidateException as e:
        print(f"Error: {e}")
        return {"error": "No se pudo generar la rutina de ejercicios. Por favor, inténtalo de nuevo."}