from django.db import models

# Create your models here.
class Usuario(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    id = models.CharField(max_length=100, primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    altura = models.FloatField(blank=True, null=True)
    ejercicio = models.IntegerField(blank=True, null=True)
    dieta = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name
        
