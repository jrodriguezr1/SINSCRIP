from django.urls import path, include
from django.contrib import admin
from siayb.views import inicio_siayb, logout_view, verificar_credenciale_siayb, mis_cursos_siayb


app_name = 'siayb'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio_siayb, name='inicio_siayb'),
    path('logout/', logout_view, name='logout_view'),
    path('verificar_credenciale_siayb/', verificar_credenciale_siayb, name='verificar_credenciale_siayb'),
    path('mis_cursos_siayb/', mis_cursos_siayb, name='mis_cursos_siayb'),
    ]