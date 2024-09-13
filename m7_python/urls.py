from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.indexView, name='index'),
    path('login/', LoginView.as_view(next_page='dashboard'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.registerView,name='register'),
    path('register_tipo/', views.register_tipoView,name='register_tipo'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('update_profile/', views.profile, name='update_profile'),
    path('new_inmueble/', views.new_inmuebleView, name='new_inmueble'),
    path('update_inmueble/', views.inmuebles_update, name='update_inmueble'),
    path('eliminar_inmueble/', views.inmuebles_delete, name='delete_inmueble'),
    path('buscar_propiedades/', views.buscar_propiedades, name='buscar_propiedades'),
    path('contacto/', views.contacto, name='contacto'),
]