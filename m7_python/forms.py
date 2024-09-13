from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comuna, Region, Inmuebles, Tipo_inmueble, ContactForm
from django.forms import ModelForm

class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class TipoForm(forms.Form):
    tipos = ((1, 'Arrendatario'),(2, 'Arrendador'),)
    tipo = forms.ChoiceField(choices=tipos)
    rut = forms.CharField(label='rut', max_length=100)
    direccion = forms.CharField(label='direccion', max_length=100)
    telefono = forms.CharField(label='telefono', max_length=100)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        
class InmuebleForm(forms.Form):
    tipos = ((1, 'Casa'),(2, 'Departamento'),(1, 'Parcela'),(2, 'Estacionamiento'),(2, 'Otro'))
    id_tipo_inmueble = forms.ChoiceField(choices=tipos)
    comunas = [(x.id,x.comuna) for x in list(Comuna.objects.filter())]
    
    def nombre_comuna(e):
        return e[1]
    comunas.sort(key=nombre_comuna)
    
    id_comuna = forms.ChoiceField(choices=comunas)
    regiones = [(x.id,x.region) for x in list(Region.objects.filter())]
    id_region = forms.ChoiceField(choices=regiones)
    nombre_inmueble = forms.CharField(label='Nombre inmueble', max_length=100)
    descripcion = forms.CharField(label='Descripcion del inmueble', max_length=100)
    m2_construido = forms.CharField(label='M2 construidos', max_length=100)
    numero_banos = forms.CharField(label='Numero de baños', max_length=100)
    numero_hab = forms.CharField(label='Numero de habitaciones', max_length=100)
    direccion = forms.CharField(label='Direccion', max_length=100)
    m2_terreno = forms.CharField(label='M2 de terreno', max_length=100)
    numero_est = forms.CharField(label='Numero de estacionamientos', max_length=100)

class InmueblesUpdateForm(forms.ModelForm):
    class Meta:
        model = Inmuebles
        fields = ['nombre_inmueble', 'descripcion', 'm2_construido', 'numero_banos', 'numero_hab', 'direccion', 'm2_terreno', 'numero_est']


class BusquedaPropiedadesForm(forms.Form):
    tipo_inmueble = forms.ModelChoiceField(queryset=Tipo_inmueble.objects.all(), required=False)
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False)
    nombre_inmueble = forms.CharField(max_length=200, required=False)
    min_m2_construido = forms.FloatField(required=False)
    max_m2_construido = forms.FloatField(required=False)
    min_numero_banos = forms.IntegerField(required=False)
    max_numero_banos = forms.IntegerField(required=False)
    min_numero_hab = forms.IntegerField(required=False)
    max_numero_hab = forms.IntegerField(required=False)
    min_m2_terreno = forms.FloatField(required=False)
    max_m2_terreno = forms.FloatField(required=False)
    min_numero_est = forms.IntegerField(required=False)
    max_numero_est = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(BusquedaPropiedadesForm, self).__init__(*args, **kwargs)
        self.fields['tipo_inmueble'].empty_label = 'Todos los tipos de inmuebles'
        self.fields['comuna'].empty_label = 'Todas las comunas'
        self.fields['region'].empty_label = 'Todas las regiones'
        
class ContactFormModelForm(ModelForm):
    class Meta:
        model = ContactForm
        fields = ['customer_email', 'customer_name', 'message']