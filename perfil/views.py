from django.shortcuts import render, redirect
from core.models import User  # Asegúrate de tener un modelo llamado Usuario
from django.views.decorators.csrf import csrf_exempt  # Importa csrf_exempt
from django.contrib.auth.decorators import login_required  # Importa login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
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
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            print('Usuario autenticado')
            return redirect('profile')
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    return render(request, 'login.html')

def logout(request):
    return render(request, 'logout.html')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        diet = request.POST.get('diet', '')
        weight = request.POST.get('weight', None)
        height = request.POST.get('height', None)
        smoker = request.POST.get('smoker', False) == 'on'
        weekly_exercise_hours = request.POST.get('weekly_exercise_hours', None)

        # Verifica si el correo electrónico ya está registrado
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'signup.html')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            diet=diet,
            weight=weight,
            height=height,
            smoker=smoker,
            weekly_exercise_hours=weekly_exercise_hours
        )

        user.save()

        # Autenticar y loguear al usuario
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirigir a la página de perfil después del registro

    return render(request, 'signup.html')

@login_required
def profile(request):
    if request.user.is_authenticated:
        # El usuario está autenticado
        return render(request, 'profile.html', {'user': request.user})
    else:
        # El usuario no está autenticado
        return redirect('login')