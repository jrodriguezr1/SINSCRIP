import json
import os
import smtplib
from datetime import date
from urllib import request

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils.html import strip_tags

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
            print('si se autentico mano')
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


def panel_posgrados2(request):
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



def panel_posgrados(request):
    usuario_id = request.session.get('usuario_id')

    try:
        usuario = Coordinaciones.objects.get(id=usuario_id)
    except Coordinaciones.DoesNotExist:
        # Si el usuario no existe, redirige al inicio de sesión
        messages.error(request, 'Usuario o contraseña incorrectos.')
        return redirect('cordins:iniciar_sesion')

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
        anio = settings.ANIO

        nombre_archivo = str(cve_program) + str(cve_estud) + 'AETA' + str(periodo) + str(anio)

        #nombre_archivo = archivo.name
        if archivo.size > 2097152:
            print('pesa mas de 2 mb')
            mensage = 'El documento PDF debe pesar menos de 2 mb'
            return JsonResponse({"message": mensage})

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

        enviar_aviso(estudiante.cve_estud)

        mensage = 'El Acta de evaluación se ha guardado para: ' + cve_estud

        return JsonResponse({"message": mensage})
    print('No es post Man')

    return JsonResponse({"message": "No se ha recibido ningún archivo o el método de solicitud no es válido."})


def  enviar_aviso(cve_estud):
    estudiante = get_object_or_404(Estudian, cve_estud=cve_estud)

    # Envía el correo electrónico
    destinatario = [estudiante.username]
    #destinatario = ['sinscripcolpos@gmail.com', estudiante.e_mailcp, 'servacadmontecillo@colpos.mx', consejero.email, coordinacion.username, 'posgradosybecas@colpos.mx']
    print(estudiante.nombres)
    asunto = 'AETA-' + str(cve_estud) + ' Registrada'
    periodo = settings.PERIODO
    anio = settings.ANIO
    mensaje = 'C O L E G I O   D E   P O S T G R A D U A D O S\n'
    mensaje += 'C A M P U S   M O N T E C I L L O\n\n'
    mensaje += 'Estimad@: ' + estudiante.nombres + ' ' + estudiante.apellidos
    mensaje += '\n\nLa coordinacion de su posgrado ha revisado su Acta de Evaluacion de Trabajo Académico\n'
    mensaje += 'Por lo que le informamos que puede acceder al sistema de inscripciones en linea (SINSEVI) http://10.0.0.90:9000/inscrip/ \n'
    mensaje += 'para realizar el proceso de inscripciones del periodo de ' + periodo + str(anio) + '.\n'
    mensaje += '\n\nATENTAMENTE\n\n'
    mensaje += 'SUBDIRECCIÓN DE EDUCACIÓN DEL CAMPUS MONTECILLO'
    mensaje_plano = strip_tags(mensaje)

    # Crear el objeto EmailMultiAlternatives
    email = EmailMultiAlternatives(
        asunto,
        str(mensaje_plano),
        'sinscripcolpos@gmail.com',
        destinatario
    )

    # Envía el correo electrónico utilizando SMTP
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_usuario = 'sinscripcolpos@gmail.com'
        smtp_password = 'murvdxcfnfroschr'  # Asegúrate de utilizar las credenciales correctas
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(smtp_usuario, smtp_password)
        smtp.sendmail(smtp_usuario, destinatario, email.message().as_bytes())

        smtp.quit()

        # Después de procesar el archivo con éxito
        return HttpResponse('Archivo recibido correctamente.')

    except smtplib.SMTPException as e:
        messages.success(request, '¡Correo electrónico no enviado, intente de nuevo!')
        return HttpResponse(f'Error al enviar el correo electrónico: {str(e)}')




