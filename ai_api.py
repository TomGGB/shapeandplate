import os
import json
import google.generativeai as genai
from dotenv import load_dotenv


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

def generate_workout_routine(data):
    system_instruction = (
        "Eres un personal trainer, se ingresarán los datos del usuario y debes darle una rutina personalizada con el nombre del ejercicio(nombre),\n"
        "duración(duracion), repeticiones(rep) si no tiene una cantidad de repeticiones no incluyas este campo en la respuesta, sesiones(sesiones), intensidad(i), puede ser 'Baja', 'Media' o 'Alta', la descipcion de cada ejercicio(desc) y una advertencia solamente si el ejercicio es de intensidad alta para no sobre exigir (advertencia),\n"
        "los ejercicios dependeran de si tiene acceso a un gymnasio o no y tambien de los datos que te entregue, que sea lo mas personalizado posible dependiendo de la cantidad de ejercicio que haga el usuario por ejemplo si no tiene acceso al gimnasio pueder recomendar hacer el ejercicio con algun objeto que pueda tener en casa \n."
        "Hay que tener en cuenta la edad y la cantidad de ejercicio semanal que hace el usuario para determinar bien la cantidad de sesiones, repeticiones y duracion de cada ejercicio, esto es lo mas importante\n"
        "Los calentamientos y enfriamientos tambien son personalizados pero no deben tener dificultad ni sesiones ni repeticiones, solamente la duración, el calentamiento debe ser el primer ejercicio y el enfriamiento el ultimo\n."
    )
    model = create_model(system_instruction)
    extra_fields = {
        'Acceso a gimnasio': "Sí" if data["gym_access"] else "No"
    }
    mensaje = create_message(data, extra_fields)
    
    try:
        response = model.generate_content(mensaje)
        return json.loads(response.text)
    except Exception as e:
        print(f"Error: {e}")
        return {"error": "No se pudo generar la rutina de ejercicios. Por favor, inténtalo de nuevo."}

import json

def generate_recipes(data, previous_recipes=None):
    formato = (
        "    \"recetas\": [\n"
        "        {\n"
        "            \"dia\": \"Lunes\",\n"
        "            \"nombre\": \"Nombre de la receta\",\n"
        "            \"tipo\": \"Desayuno\",\n"
        "            \"ingredientes\": [\n"
        "                \"Ingrediente 1\",\n"
        "                \"Ingrediente 2\",\n"
        "                \"Ingrediente 3\"\n"
        "            ],\n"
        "            \"instrucciones\": [\n"
        "                \"Paso 1\",\n"
        "                \"Paso 2\",\n"
        "                \"Paso 3\"\n"
        "            ],\n"
        "            \"tiempo\": \"15 minutos\",\n"
        "            \"dificultad\": \"Media\",\n"
        "            \"desc\": \"Descripción de la receta\"\n"
        "        }\n"
        "    ]\n"
        "}"
    )
    system_instruction = (
        "Eres un chef, se ingresarán los datos del usuario y debes darle recetas (recetas) personalizadas para toda la semana con el dia de cada receta(dia), el nombre de la receta(nombre) y tipo de receta si es que es desayuno, almuerzo o cena(tipo),\n"
        "ingredientes(ingredientes), instrucciones(instrucciones), tiempo de preparación(tiempo), dificultad(dificultad), puede ser 'Fácil', 'Media' o 'Difícil', la descripción de la receta(desc) y una advertencia solamente si la receta es de dificultad alta para no complicar mucho (advertencia),\n"
        "las recetas dependeran de la dieta del usuario y tambien de los datos que te entregue, que sea lo mas personalizado posible dependiendo de la cantidad de ejercicio que haga el usuario y tambien incluye el desayuno, almuerzo, cena y colaciones o cantidades de proteina, carbohidratos y grasas que debe consumir en el día.\n"
        "Debes dar una variedad de recetas para que el usuario no se aburra de comer lo mismo, además de especificar si es desayuno, almuerzo o cena. También debes tener en cuenta si el usuario fuma o no para darle recetas más saludables. Es importante que el nombre de los alimentos o ingredientes sea el que se utiliza en Chile, ya que la aplicación es para público de este país.\n"
        "La respuesta debe tener el siguiente formato: \n"
        "Se adjuntarán recetas ya previamente generadas para tenerlas en consideracion al generarlas que no se repitan.\n"
        + formato
    )
    model = create_model(system_instruction)
    extra_fields = {
        'Rutina del usuario': data["routine"],
        'Recetas previas': previous_recipes if previous_recipes else "Ninguna"
    }
    mensaje = create_message(data, extra_fields)
    
    try:
        response = model.generate_content(mensaje)
        new_recipes = json.loads(response.text)["recetas"]
        
        if previous_recipes:
            previous_recipes_set = {json.dumps(recipe, sort_keys=True) for recipe in previous_recipes}
            unique_new_recipes = [recipe for recipe in new_recipes if json.dumps(recipe, sort_keys=True) not in previous_recipes_set]
        else:
            unique_new_recipes = new_recipes
        
        return {"recetas": unique_new_recipes}
    except Exception as e:
        print(f"Error: {e}")