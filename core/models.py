from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

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

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    diet = models.CharField(max_length=100, blank=True, null=True)
    weight = models.IntegerField(("weight in kg"), blank=True, null=True)
    height = models.IntegerField(("height in cm"), blank=True, null=True)
    smoker = models.BooleanField(default=False)
    weekly_exercise_hours = models.IntegerField(("weekly exercise hours"), blank=True, null=True)
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

    def __str__(self):
        return f"Routine for {self.user.first_name} {self.user.last_name}"

class FoodRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.JSONField()

    def __str__(self):
        return f"Recipe for {self.user.first_name} {self.user.last_name}"