from django.shortcuts import render, redirect
from .models import Usuario  # Asegúrate de tener un modelo llamado Usuario
from django.views.decorators.csrf import csrf_exempt  # Importa csrf_exempt
from google.cloud import bigquery
from dotenv import load_dotenv
import os
import uuid
import tempfile
import json

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Decodifica el JSON de las credenciales de Google Cloud
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
credentials_dict = json.loads(credentials_json)

# Crea un archivo temporal para las credenciales de Google Cloud
with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
    json.dump(credentials_dict, temp_file)
    temp_file_path = temp_file.name

# Configura la variable de entorno para las credenciales de Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path

# Inicializa un cliente para interactuar con BigQuery
client = bigquery.Client()

def login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'logout.html')

def signup(request):
    return render(request, 'signup.html')

def profile(request):
    return render(request, 'profile.html')
@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        edad = request.POST['edad']
        altura = request.POST['altura']
        ejercicio = request.POST['ejercicio']
        dieta = request.POST['dieta']

        # Construye un diccionario con los datos a insertar
        data = {
            #se crea un UID para cada usuario
            "id": str(uuid.uuid4()),
            "nombre": nombre,
            "apellidos": apellidos,
            "edad": edad,
            "altura": altura,
            "ejercicio": ejercicio,
            "dieta": dieta
        }

        # Define el ID de la tabla (ajusta según tu proyecto y conjunto de datos)
        table_id = "shapeandplate.workout.usuario"

        # Inserta los datos en la tabla
        errors = client.insert_rows_json(table_id, [data])

        #Tambien guardar los datos en la base de datos de Django
        usuario = Usuario(id=data["id"], nombre=data["nombre"], apellidos=data["apellidos"], edad=data["edad"], altura=data["altura"], ejercicio=data["ejercicio"], dieta=data["dieta"])
        usuario.save()

        if errors == []:
            # Redirigir a una página de confirmación o de inicio
            return redirect('workout')
        else:
            # Manejar errores, por ejemplo, mostrar un mensaje de error al usuario
            return render(request, 'error.html', {'error_message': 'Error al guardar los datos'})

    return render(request, 'workout.html')