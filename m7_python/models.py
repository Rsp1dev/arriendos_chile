from django.db import models
from django.contrib.auth.models import User
import uuid

class Usuario(models.Model):
    id_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True,)

class Tipo_inmueble(models.Model):
    tipo_inmueble = models.TextField()

class Comuna(models.Model): 
    comuna = models.TextField()

class Region(models.Model):
    region = models.TextField()

class Tipo_user(models.Model):
    tipo_user = models.TextField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_tipo_user = models.ForeignKey('m7_python.Tipo_user', on_delete=models.CASCADE, null=True,)
    rut = models.TextField()
    direccion = models.TextField()
    telefono = models.TextField()
    correo = models.TextField()

class Inmuebles(models.Model):
    id_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    id_tipo_inmueble = models.ForeignKey('m7_python.Tipo_inmueble',on_delete=models.CASCADE, null=True)
    id_comuna = models.ForeignKey('m7_python.Comuna', on_delete=models.CASCADE, null=True,)
    id_region = models.ForeignKey('m7_python.Region', on_delete=models.CASCADE, null=True)
    nombre_inmueble = models.TextField()
    descripcion = models.TextField(max_length=200)
    m2_construido = models.FloatField()
    numero_banos = models.IntegerField(default=0) 
    numero_hab = models.IntegerField(default=0)   
    direccion = models.CharField(max_length=200)
    #agregados datos faltantes
    m2_terreno = models.FloatField(default=0)
    numero_est = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='inmuebles', blank=True, null=True)
    
class ContactForm(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=64)
    message = models.TextField()