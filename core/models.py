from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField(blank=True, null=True)
    diet = models.CharField(max_length=100, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)  # Campo para almacenar alergias
    weight = models.IntegerField(("weight in kg"), blank=True, null=True)
    height = models.IntegerField(("height in cm"), blank=True, null=True)
    smoker = models.BooleanField(default=False)
    weekly_exercise_hours = models.IntegerField(("weekly exercise hours"), blank=True, null=True)
    imc = models.FloatField(("imc"), blank=True, null=True)
    goal = models.CharField(max_length=100, blank=True, null=True)
    gym_access = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

class ExerciseRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routine = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    progress = models.JSONField(default=dict)
    exercise_times = models.JSONField(default=dict)

    def __str__(self):
        return f"Rutina de {self.user.first_name} {self.user.last_name} creada el {self.created_at}"

class FoodRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.JSONField()

    def __str__(self):
        return f"Recipe for {self.user.first_name} {self.user.last_name}"