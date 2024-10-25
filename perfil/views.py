import os
import uuid
import tempfile
import json

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, smart_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from core.models import User
from google.cloud import bigquery
from dotenv import load_dotenv


# Carga las variables de entorno desde el archivo .env
load_dotenv()


def verify_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Tu cuenta ha sido verificada exitosamente. Ahora puedes iniciar sesión.')
        return redirect('login')
    else:
        messages.error(request, 'El enlace de verificación no es válido.')
        return redirect('signup')


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
            messages.success(request, 'Has iniciado sesión correctamente.')
            return redirect('profile')
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    return render(request, 'login.html')
    
def logout(request):
    auth_logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
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
        user.is_active = False  # Desactivar la cuenta hasta que se verifique el correo
        user.save()

        # Generar el token de verificación
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = request.build_absolute_uri(f'/perfil/verify/{uid}/{token}/')

        # Enviar el correo de verificación
        email_subject = 'Verificación de Cuenta'
        email_body = render_to_string('verification_email.html', {
            'verification_link': verification_link,
            'user': user,
        })
        send_mail(
            email_subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=email_body
        )

        messages.success(request, 'Registro exitoso. Por favor, verifica tu correo electrónico para activar tu cuenta.')
        return redirect('login')

    return render(request, 'signup.html')

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.age = request.POST.get('age', user.age)
        user.email = request.POST.get('email', user.email)
        user.diet = request.POST.get('diet', user.diet)
        user.weight = request.POST.get('weight', user.weight)
        user.height = request.POST.get('height', user.height)
        user.smoker = 'smoker' in request.POST
        user.weekly_exercise_hours = request.POST.get('weekly_exercise_hours', user.weekly_exercise_hours)
        user.gym_access = 'gym_access' in request.POST
        
        imc = request.POST.get('imc', user.imc)
        goal = request.POST.get('goal', user.goal)
        if imc:
            imc = imc.replace(',', '.')  # Reemplaza la coma por un punto
            user.imc = float(imc)  # Convierte la cadena a un número
        
        user.goal = request.POST.get('goal', user.goal)

        user.save()
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('profile')

    context = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'age': user.age,
        'diet': user.diet,
        'weight': user.weight,
        'height': user.height,
        'smoker': user.smoker,
        'weekly_exercise_hours': user.weekly_exercise_hours,
        'imc': user.imc,
        'goal': user.goal,
        'gym_access': user.gym_access,
    }
    return render(request, 'profile.html', context)

def password_reset(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(f'/perfil/reset/{uid}/{token}/')
            email_subject = 'Restablecimiento de Contraseña'
            email_body = render_to_string('password_reset_email.html', {
                'reset_link': reset_link,
                'user': user,
            })
            send_mail(
                email_subject,
                '',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=email_body  # Asegúrate de enviar el mensaje HTML
            )
            messages.success(request, 'Se ha enviado un enlace de restablecimiento de contraseña a tu correo electrónico.')
        except User.DoesNotExist:
            messages.error(request, 'No se encontró una cuenta con ese correo electrónico.')
        return redirect('password_reset')
    return render(request, 'password_reset.html')

def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST['new_password']
            new_password_confirm = request.POST['new_password_confirm']
            if new_password == new_password_confirm:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Tu contraseña ha sido restablecida exitosamente.')
                return redirect('login')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
        return render(request, 'password_reset_confirm.html', {'validlink': True})
    else:
        messages.error(request, 'El enlace de restablecimiento de contraseña no es válido.')
        return render(request, 'password_reset_confirm.html', {'validlink': False})