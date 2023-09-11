import json
import os
from datetime import date
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from SINSCRIP import settings
from capcursapp.models import Coordinaciones
from inscrip.models import Estudian



# Create your views here.
def iniciar_sesion(request):
    # Cerrar sesión (antes de redireccionar)
    return render(request, 'inicio_cordins.html')

def logout_view(request):
    logout(request)
    return redirect('cordins:iniciar_sesion')

def verificar_credenciales(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['usuario_id'] = user.id
            return redirect('cordins:panel_posgrados')
        else:
            # Las credenciales son inválidas
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'inicio_cordins.html')
    else:
        return render(request, 'inicio_cordins.html')

def estudiante_to_dict(estudiante):

    return {
        'id': estudiante.id,
        'cve_estud': estudiante.cve_estud,
        'nombres': estudiante.nombres,
        'apellidos': estudiante.apellidos,
        'cve_campus': estudiante.cve_campus,
        'cve_institu': estudiante.cve_institu,
        'cve_program': estudiante.cve_program,
        'periingr': estudiante.periingr,
        'fechingr': estudiante.fechingr,
        'cve_sexo': estudiante.cve_sexo,
        'e_mail': estudiante.e_mail,
        'e_mailcp': estudiante.e_mailcp,
        'aeta': estudiante.aeta,
        'consejop': estudiante.consejop,
        'username': estudiante.username,
        'password': estudiante.password,
        'niveestu': estudiante.niveestu,
        'cont_veces': estudiante.cont_veces,
        'cont_final': estudiante.cont_final,
    }

from django.core.serializers.json import DjangoJSONEncoder


def custom_json_serializer(obj):
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError("Object of type '{}' is not JSON serializable".format(type(obj).__name__))


def panel_posgrados(request):
    usuario_id = request.session.get('usuario_id')
    usuario = Coordinaciones.objects.get(id=usuario_id)
    periodo = settings.PERIODO
    clave = ['MAESTRIA', 'DOCTORADO']
    valor = ['MAESTRIA', 'DOCTORADO']
    categorias = dict(zip(clave, valor))

    if usuario.cve_program == 'EST':
        print('es estadistica man')
        estudiantes = Estudian.objects.filter(Q(cve_program='ECD') | Q(cve_program='EST'))
    else:
        estudiantes = Estudian.objects.filter(cve_program=usuario.cve_program)

    data = [{'cve_estud': est.cve_estud, 'niveestu': est.niveestu, 'nombres': est.nombres,
             'apellidos': est.apellidos, 'consejop': est.consejop,
             'aeta': est.aeta} for est in estudiantes]

    return render(request, 'panel_posgra.html',
                  {'usuario': usuario, 'periodo': periodo, 'categorias': categorias, 'data': data})


def estudiantes_por_categoria(request):
    print('aqui van filtrados')
    usuario_id = request.session.get('usuario_id')
    usuario = Coordinaciones.objects.get(id=usuario_id)


    if request.method == 'GET':
        categoria_seleccionada = request.GET.get('categoria')
        if usuario.cve_program == 'EST':
            print('es estadistica man')
            estudiantes = Estudian.objects.filter(Q(cve_program='ECD') | Q(cve_program='EST'),
                                                  niveestu=categoria_seleccionada)
        else:
            estudiantes = Estudian.objects.filter(cve_program=usuario.cve_program, niveestu=categoria_seleccionada)

        data = [{'cve_estud': est.cve_estud, 'nombres': est.nombres,
                 'apellidos': est.apellidos, 'consejop': est.consejop,
                 'aeta': est.aeta} for est in estudiantes]
        return JsonResponse(data, safe=False)

def actualizar_checkbox(request):
    if request.method == 'POST':
        matricula = request.POST.get('cve_estud')
        estudiante = Estudian.objects.filter(cve_estud=matricula).first()
        print(estudiante.nombres, estudiante.apellidos)

        # Cambiar el valor del campo checkbox
        estudiante.aeta = not estudiante.aeta
        estudiante.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})



def upload_pdf(request, student_id):
    if request.method == 'POST':
        # Obtener el archivo PDF del request
        print('SI es post')
        pdf_file = request.FILES.get('pdf', None)

        if not pdf_file:
            return JsonResponse({'error': 'No se recibió el archivo PDF'}, status=400)

        if pdf_file.size > 2097152:
            return JsonResponse({'error': 'El archivo seleccionado supera el tamaño máximo de 2 MB'}, status=400)

        # Procesar y guardar el archivo en el servidor
        try:
            with open(f'/SINS_CRIP/AETA_2023/{student_id}_archivo.pdf', 'wb') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)
        except Exception as e:
            return JsonResponse({'error': 'Error al guardar el archivo en el servidor'}, status=500)

        return JsonResponse({'message': 'Archivo PDF subido correctamente'}, status=200)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def recibir_archivo(request):
    if request.method == "POST":
        cve_estud = request.POST.get('cve_estud')
        cve_program = request.POST.get('cve_program')

        print('Estudiante: ', cve_estud,' ', cve_program)

        #archivo = request.FILES["archivo"]
        archivo = request.FILES["pdf"]
        # cve_program matricula periodo agno
        # COA_12033059_VERANO_2023
        periodo = settings.PERIODO

        nombre_archivo = cve_program + cve_estud + 'AETA' + periodo

        #nombre_archivo = archivo.name
        if archivo.size > 2097152:
            print('pesa menos de 2')
            return JsonResponse({'error': 'El archivo seleccionado supera el tamaño máximo de 2 MB'}, status=400)

        # Ruta donde se almacenarán los archivos (directorio 'boletas_2023' en el directorio de medios de Django)
        ruta_archivos = os.path.join("AETA_2023", nombre_archivo)

        # Guardar el archivo en el servidor
        with open(ruta_archivos, "wb") as destino:
            for chunk in archivo.chunks():
                destino.write(chunk)

        # Aquí puedes realizar otras operaciones con el archivo si es necesario

        estudiante = Estudian.objects.get(cve_estud=cve_estud, cve_program=cve_program)
        estudiante.aeta = True  # O asigna el valor que corresponda
        estudiante.save()  # Guarda los cambios en la base de datos

        mensage = 'El Acta de evaluación se ha guardado para: ' + cve_estud

        return JsonResponse({"message": mensage})
    print('No es post Man')

    return JsonResponse({"message": "No se ha recibido ningún archivo o el método de solicitud no es válido."})

