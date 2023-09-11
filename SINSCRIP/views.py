from django.shortcuts import render
from django.conf import settings

def panel_control(request):
    template_name = 'panelde_control.html'
    print(settings.TEMPLATES[0]['DIRS'])  # Imprime la ruta de búsqueda de las plantillas
    return render(request, template_name)


