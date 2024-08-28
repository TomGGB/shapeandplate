from django.shortcuts import render, redirect
from core.models import User  # Asegúrate de tener un modelo llamado Usuario
from django.views.decorators.csrf import csrf_exempt  # Importa csrf_exempt
from django.contrib.auth.decorators import login_required  # Importa login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
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

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        
        if email is None or password is None:
            messages.error(request, 'Correo electrónico y contraseña son requeridos.')
            return render(request, 'login.html')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            print('Usuario autenticado')
            return redirect('profile')
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    return render(request, 'login.html')
    
def logout(request):
    auth_logout(request)
    return redirect('login')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden. Por favor, inténtalo de nuevo.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado. Por favor, usa otro correo.')
            return redirect('signup')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'signup.html')

def profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.diet = request.POST.get('diet', user.diet)
        user.weight = request.POST.get('weight', user.weight)
        user.height = request.POST.get('height', user.height)
        user.smoker = 'smoker' in request.POST
        user.weekly_exercise_hours = request.POST.get('weekly_exercise_hours', user.weekly_exercise_hours)
        user.goal = request.POST.get('goal', user.goal)

        user.save()
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('profile')

    context = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'diet': user.diet,
        'weight': user.weight,
        'height': user.height,
        'smoker': user.smoker,
        'weekly_exercise_hours': user.weekly_exercise_hours,
        'objetivo': user.goal,
    }
    return render(request, 'profile.html', context)

def password_reset(request):
    return render(request, 'password_reset.html')