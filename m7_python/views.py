from django.shortcuts import render, redirect
from m7_python.models import *
from m7_python.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BusquedaPropiedadesForm
from .models import Inmuebles
import json


# Create your views here.
def registerView(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return HttpResponseRedirect('/register_tipo?user='+str(form.cleaned_data['username']))
    else:
        form = UserForm()
    return render(request,'registration/register.html',{'form':form})

def register_tipoView(request):
    username = request.GET['user']
    if request.method == 'POST':
        form = TipoForm(request.POST)
        if form.is_valid():
            form = TipoForm(request.POST)
            print(form)
            tipo = form.cleaned_data['tipo']
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            user = User.objects.filter(username=username)[0]
            tipo_user = Tipo_user.objects.filter(id=int(tipo))[0]
            datos = Profile(user=user,id_tipo_user=tipo_user,rut=rut,direccion=direccion,telefono=telefono)
            datos.save()
            return HttpResponseRedirect('/login/')
    else:
        form = TipoForm()
    return render(request,'registration/register_tipo.html',{'form':form})

@login_required
def dashboardView(request):
    username = request.user
    current_user = request.user
    Inm = Inmuebles.objects.filter(id_user_id=current_user.id)    
    return render(request,'dashboard.html',{'inmuebles':Inm})

def indexView(request):
    Inm = Inmuebles.objects.all()
    return render(request,'index.html',{'inmuebles': Inm})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        u_form = UserUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form}
    return render(request,'registration/update_profile.html',context)

@login_required 
def new_inmuebleView(request):
    if request.method == "POST":
        u_form = InmuebleForm(request.POST)
        #print(u_form.cleaned_data)
        if u_form.is_valid():
            id_tipo_inmueble = u_form.cleaned_data['id_tipo_inmueble']
            id_comuna = u_form.cleaned_data['id_comuna']
            id_region = u_form.cleaned_data['id_region']
            nombre_inmueble = u_form.cleaned_data['nombre_inmueble']
            descripcion = u_form.cleaned_data['descripcion']
            m2_construido = u_form.cleaned_data['m2_construido']
            numero_banos = u_form.cleaned_data['numero_banos']
            numero_hab = u_form.cleaned_data['numero_hab']
            direccion = u_form.cleaned_data['direccion']
            m2_terreno = u_form.cleaned_data['m2_terreno']
            numero_est = u_form.cleaned_data['numero_est']
            #print(u_form.cleaned_data)
            tipo_inmueble = Tipo_inmueble.objects.filter(id=int(id_tipo_inmueble))[0]
            comuna = Comuna.objects.filter(id=int(id_comuna))[0]
            reg = Region.objects.filter(id=int(id_region))[0]
            current_user = request.user
            user = User.objects.filter(id=current_user.id)
            inm = Inmuebles(id_tipo_inmueble=tipo_inmueble,
                            id_comuna = comuna,
                            id_region = reg,
                            nombre_inmueble = nombre_inmueble,
                            descripcion = descripcion,
                            m2_construido = m2_construido,
                            numero_banos = numero_banos,
                            numero_hab = numero_hab,
                            direccion = direccion,
                            m2_terreno = m2_terreno,
                            numero_est = numero_est,
            )

            print(user)
            inm.id_user_id = current_user.id
            inm.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        u_form = InmuebleForm()

    context = {'u_form': u_form}
    return render(request,'new_inmueble.html',context)

@login_required    
def inmuebles_update(request):
    inmueble_id = request.GET['id_inmueble']
    if request.method == 'POST':
        inmueble_id = request.GET['id_inmueble']
        inmueble = Inmuebles.objects.filter(id=inmueble_id).first()
        u_form = InmueblesUpdateForm(request.POST,instance=inmueble)
        if u_form.is_valid():
            u_form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        inmueble = Inmuebles.objects.filter(id=inmueble_id).first()
        u_form = InmueblesUpdateForm(instance=inmueble)

    context={'u_form': u_form}
    return render(request,'registration/update_profile.html',context)


@login_required
def inmuebles_delete(request):
    inmueble_id = request.GET['id_inmueble']
    record = Inmuebles.objects.get(id=inmueble_id)
    record.delete()      
    return HttpResponseRedirect('/dashboard/')


def buscar_propiedades(request):
    if request.method == 'POST':
        form = BusquedaPropiedadesForm(request.POST)
        if form.is_valid():
            tipo_inmueble = form.cleaned_data['tipo_inmueble']
            comuna = form.cleaned_data['comuna']
            region = form.cleaned_data['region']
            nombre_inmueble = form.cleaned_data['nombre_inmueble']
            min_m2_construido = form.cleaned_data['min_m2_construido']
            max_m2_construido = form.cleaned_data['max_m2_construido']
            min_numero_banos = form.cleaned_data['min_numero_banos']
            max_numero_banos = form.cleaned_data['max_numero_banos']
            min_numero_hab = form.cleaned_data['min_numero_hab']
            max_numero_hab = form.cleaned_data['max_numero_hab']
            min_m2_terreno = form.cleaned_data['min_m2_terreno']
            max_m2_terreno = form.cleaned_data['max_m2_terreno']
            min_numero_est = form.cleaned_data['min_numero_est']
            max_numero_est = form.cleaned_data['max_numero_est']

            # Cargar datos de inmuebles desde el archivo JSON
            with open('inmuebles_data.json') as f:
                inmuebles_data = json.load(f)

            # Cargar datos de tipos de inmuebles desde el archivo JSON
            with open('tipo_inmueble_data.json') as f:
                tipo_inmueble_data = json.load(f)

            # Cargar datos de tipos de usuarios desde el archivo JSON
            with open('tipo_usuario_data.json') as f:
                tipo_usuario_data = json.load(f)

            # Crear objetos de tipo Inmueble, Tipo_inmueble y Tipo_usuario
            inmuebles = []
            tipos_inmueble = []
            tipos_usuario = []

            for inmueble in inmuebles_data:
                inmueble_obj = Inmuebles(
                    nombre_inmueble=inmueble['fields']['nombre_inmueble'],
                    descripcion=inmueble['fields']['descripcion'],
                    m2_construido=inmueble['fields']['m2_construido'],
                    numero_banos=inmueble['fields']['numero_banos'],
                    direccion=inmueble['fields']['direccion'],
                    m2_terreno=inmueble['fields']['m2_terreno'],
                    numero_est=inmueble['fields']['numero_est'],
                    id_comuna_id=inmueble['fields']['id_comuna_id'],
                    id_region_id=inmueble['fields']['id_region_id'],
                    id_tipo_inmueble_id=inmueble['fields']['id_tipo_inmueble_id'],
                    id_user_id=inmueble['fields']['id_user_id']
                )
                inmuebles.append(inmueble_obj)

            # Filtrar inmuebles según los criterios de búsqueda
            filtered_inmuebles = []
            for inmueble in inmuebles:
                if (inmueble.tipo_inmueble == tipo_inmueble and
                    inmueble.comuna == comuna and
                    inmueble.region == region and
                    inmueble.nombre_inmueble == nombre_inmueble and
                    inmueble.m2_construido >= min_m2_construido and
                    inmueble.m2_construido <= max_m2_construido and
                    inmueble.numero_banos >= min_numero_banos and
                    inmueble.numero_banos <= max_numero_banos and
                    inmueble.numero_hab >= min_numero_hab and
                    inmueble.numero_hab <= max_numero_hab and
                    inmueble.m2_terreno >= min_m2_terreno and
                    inmueble.m2_terreno <= max_m2_terreno and
                    inmueble.numero_est >= min_numero_est and
                    inmueble.numero_est <= max_numero_est):
                    filtered_inmuebles.append(inmueble)

            # Renderizar la plantilla con los resultados filtrados
            return render(request, 'busqueda_resultados.html', {'inmuebles': filtered_inmuebles})
    else:
        form = BusquedaPropiedadesForm()
    return render(request, 'buscar_propiedades.html', {'form': form})

def contacto(request):
    if request.method == 'POST':
        form = ContactFormModelForm(request.POST)
        if form.is_valid():
            
            contact_form = ContactForm.objects.create(**form.cleaned_data)
            
            return HttpResponseRedirect('/exito')
    
    else:
        form = ContactFormModelForm()
        
    return render(request, 'contacto.html', {'form':form})

def exito(request):
    return render(request, 'success.html', {})
