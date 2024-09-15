import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import requests

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def configure_api():
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)

def create_model(system_instruction):
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

def create_message(data, extra_fields):
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
    )
    for field, value in extra_fields.items():
        mensaje += f'{field}: {value} \n'
    return mensaje

def get_exercise_image(exercise_name):
    api_key = os.getenv('PEXELS_API_KEY')
    url = f"https://api.pexels.com/v1/search?query={exercise_name}&per_page=1"
    headers = {
        "Authorization": api_key
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['photos']:
            return data['photos'][0]['src']['landscape']
    return None

def generate_workout_routine(data):
    system_instruction = (
        "Eres un personal trainer experto con amplia experiencia en crear rutinas personalizadas. Analiza cuidadosamente los datos del usuario y crea una rutina de ejercicios altamente personalizada siguiendo estas pautas:\n\n"
        "1. Adapta la intensidad y complejidad de los ejercicios según la edad, peso, IMC y horas de ejercicio semanal del usuario.\n"
        "2. Para usuarios mayores de 50 años o con poco ejercicio semanal, enfócate en ejercicios de baja impacto y fortalecimiento gradual.\n"
        "3. Si el usuario tiene sobrepeso (IMC > 25), incluye ejercicios que sean seguros para sus articulaciones.\n"
        "4. Ajusta la dificultad: para principiantes (0-2 horas semanales), usa intensidad 'Baja'; para intermedios (3-5 horas), 'Media'; para avanzados (6+ horas), 'Alta'.\n"
        "5. Considera el objetivo del usuario (pérdida de peso, tonificación, etc.) al seleccionar los tipos de ejercicios.\n"
        "6. Si el usuario es fumador, incluye más ejercicios cardiovasculares y de capacidad pulmonar.\n"
        "7. Adapta los ejercicios según el acceso a gimnasio, sugiriendo alternativas con objetos caseros si no tiene acceso.\n\n"
        "Para cada ejercicio, proporciona:\n"
        "1. nombre: Proporciona un nombre muy descriptivo y específico en español para el ejercicio, incluyendo detalles sobre la posición del cuerpo, el movimiento y cualquier equipo utilizado. Por ejemplo, 'Sentadillas profundas con salto y brazos extendidos' o 'Flexiones de pecho en declive con pies elevados en banco'.\n"
        "2. nombre_en: El nombre del ejercicio en inglés, igualmente muy descriptivo y específico. IMPORTANTE: Siempre comienza con 'Person doing' o 'Person performing' para asegurar que la búsqueda de imágenes muestre a una persona realizando el ejercicio. Por ejemplo, 'Person doing deep jump squats with extended arms' o 'Person performing decline push-ups with feet elevated on bench'.\n"
        "3. duracion: Duración del ejercicio (NO incluir para calentamiento y enfriamiento).\n"
        "4. rep: Número de repeticiones (si aplica, NO incluir para calentamiento y enfriamiento).\n"
        "5. sesiones: Número de series o sesiones (NO incluir para calentamiento y enfriamiento).\n"
        "6. i: Intensidad (puede ser 'Baja', 'Media' o 'Alta', NO incluir para calentamiento y enfriamiento).\n"
        "7. desc: Una descripción detallada de cómo realizar el ejercicio correctamente, incluyendo la posición inicial, el movimiento y la posición final. Para calentamiento y enfriamiento, incluye una descripción general de las actividades a realizar.\n"
        "8. advertencia: Incluye una advertencia si el ejercicio es de intensidad alta o requiere precauciones especiales.\n\n"
        "Los ejercicios deben ser personalizados según si el usuario tiene acceso a un gimnasio o no. Si no tiene acceso, sugiere alternativas con objetos que pueda tener en casa, siendo específico sobre qué objetos usar.\n"
        "Ten en cuenta la edad y la cantidad de ejercicio semanal que hace el usuario para determinar la cantidad de sesiones, repeticiones y duración de cada ejercicio.\n"
        "El calentamiento debe ser el primer ejercicio y el enfriamiento el último. Estos NO deben tener intensidad, sesiones, repeticiones ni duración, solo una descripción detallada.\n"
        "Asegúrate de que cada nombre de ejercicio sea único, muy descriptivo y específicamente relacionado con la acción física del ejercicio, tanto en español como en inglés. Evita nombres genéricos o poco descriptivos."
    )
    model = create_model(system_instruction)
    extra_fields = {
        'Acceso a gimnasio': "Sí" if data["gym_access"] else "No"
    }
    mensaje = create_message(data, extra_fields)
    
    try:
        response = model.generate_content(mensaje)
        routine = json.loads(response.text)
        
        # Añadir imágenes a cada ejercicio
        for exercise in routine['rutina']:
            image_url = get_exercise_image(exercise['nombre_en'])
            if image_url:
                exercise['imgurl'] = image_url
        
        return routine
    except Exception as e:
        print(f"Error: {e}")
        return {"error": "No se pudo generar la rutina de ejercicios. Por favor, inténtalo de nuevo."}

def generate_recipes(data, previous_recipes=None):
    system_instruction = (
        "Eres un chef nutricionista experto. Crea un plan de alimentación semanal altamente personalizado basado en los datos del usuario y su rutina de ejercicios, siguiendo estas pautas:\n\n"
        "1. Ajusta las calorías y macronutrientes según el objetivo del usuario (pérdida de peso, ganancia de masa muscular, etc.).\n"
        "2. Considera la edad, peso, altura e IMC para determinar las necesidades nutricionales específicas.\n"
        "3. Adapta las recetas a la dieta del usuario (vegetariana, vegana, sin gluten, etc.).\n"
        "4. Incluye alimentos que complementen la rutina de ejercicios, proporcionando los nutrientes necesarios para la recuperación muscular.\n"
        "5. Si el usuario es fumador, incorpora alimentos ricos en antioxidantes y que promuevan la salud pulmonar.\n"
        "6. Ajusta las porciones y frecuencia de comidas según las horas de ejercicio semanal del usuario.\n"
        "7. Utiliza ingredientes y nombres de alimentos comunes en Chile.\n"
        "8. Proporciona una variedad de recetas para evitar la monotonía, incluyendo desayunos, almuerzos, cenas y colaciones.\n\n"
        "Para cada receta, incluye:\n"
        "1. dia: Día de la semana.\n"
        "2. nombre: Nombre descriptivo de la receta.\n"
        "3. tipo: 'Desayuno', 'Almuerzo', 'Cena' o 'Colación'.\n"
        "4. ingredientes: Lista de ingredientes con cantidades.\n"
        "5. instrucciones: Pasos detallados para preparar la receta.\n"
        "6. tiempo: Tiempo de preparación.\n"
        "7. dificultad: 'Fácil', 'Media' o 'Difícil'.\n"
        "8. desc: Breve descripción de la receta y sus beneficios nutricionales.\n"
        "9. advertencia: Solo para recetas de dificultad alta o que requieran precauciones especiales.\n\n"
        "Asegúrate de que las recetas sean variadas y no se repitan con las recetas previas proporcionadas."
    )
    model = create_model(system_instruction)
    extra_fields = {
        'Rutina de ejercicios': data["routine"],
        'Recetas previas': previous_recipes if previous_recipes else "Ninguna"
    }
    mensaje = create_message(data, extra_fields)
    
    try:
        response = model.generate_content(mensaje)
        recipes_data = json.loads(response.text)
        
        # Verifica si 'plan_semanal' está en recipes_data
        if 'plan_semanal' not in recipes_data:
            print(f"Respuesta inesperada: {recipes_data}")
            return {"error": "Formato de respuesta inesperado. Por favor, inténtelo de nuevo."}
        
        new_recipes = recipes_data['plan_semanal']
        
        if previous_recipes:
            previous_recipes_set = {json.dumps(recipe, sort_keys=True) for recipe in previous_recipes}
            unique_new_recipes = [recipe for recipe in new_recipes if json.dumps(recipe, sort_keys=True) not in previous_recipes_set]
        else:
            unique_new_recipes = new_recipes
        
        return {"plan_semanal": unique_new_recipes}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": f"No se pudieron generar las recetas: {str(e)}"}