from django.contrib import admin
from .models import Inmuebles, Tipo_inmueble, Comuna, Region, Tipo_user, Profile, Usuario

admin.site.register(Inmuebles)
admin.site.register(Tipo_inmueble)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Tipo_user)
admin.site.register(Profile)
admin.site.register(Usuario)
