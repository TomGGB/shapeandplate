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
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
            "Eres un personal trainer, se ingresarán los datos del usuario y debes darle una rutina personalizada con el nombre del ejercicio(nombre),\n"
            "duración(duracion), repeticiones(rep) si no tiene una cantidad de repeticiones no incluyas este campo en la respuesta, sesiones(sesiones), intensidad(i), puede ser 'Baja', 'Media' o 'Alta', la descipcion de cada ejercicio(desc) y una advertencia solamente si el ejercicio es de intensidad alta para no sobre exigir (advertencia),\n"
            "los ejercicios dependeran de si tiene acceso a un gymnasio o no y tambien de los datos que te entregue, que sea lo mas personalizado posible dependiendo de la cantidad de ejercicio que haga el usuario y tambien incluye el calentamiento y enfriamiento como ultimo ejercicio\n."
            "Hay que tener en cuenta la edad y la cantidad de ejercicio semanal que hace el usuario para determinar bien la cantidad de sesiones, repeticiones y duracion de cada ejercicio, esto es lo mas importante"
        )
    )

    mensaje = (
        f'Datos del usuario: \n'
        f'Edad: {data["edad"]} \n'
        f'Altura: {data["altura"]} \n'
        f'Peso: {data["peso"]} \n'
        f'Horas de ejercicio que el usuario hace en la semana: {data["ejercicio_semanal"]} \n'
        f'Dieta: {data["dieta"]} \n'
        f'Indice de masa corporal: {data["imc"]} \n'
        f'Objetivo: {data["objetivo"]} \n'
        f'Fumador: {"Sí" if data["smoker"] else "No"}'
        f'Acceso a gimnasio: {"Sí" if data["gym_access"] else "No"}'
    )
    
    try:
        response = model.generate_content(mensaje)
        return json.loads(response.text)
    except Exception as e:
        print(f"Error: {e}")
        return {"error": "No se pudo generar la rutina de ejercicios. Por favor, inténtalo de nuevo."}