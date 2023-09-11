import json
import smtplib
import os
from django.contrib.auth import logout, login
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from inscrip.models import Coordinaciones, estudiante_consejero, Capcurs, Catacurs, Becarios, Asistira, Catabeca, \
    Imparegu, Estudian, Sinsevi
from inscrip.models import Academic
from inscrip.forms import AsistiraForm, SinseviForm
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render



# Create your views here.
def inicio_sesionE(request):
    # Cerrar sesión (antes de redireccionar)
    return render(request, 'inicio_sesionEst.html')


def logout_view(request):
    logout(request)
    return redirect('inscrip:inicio_sesionE')


def verificar_credencialEst(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('usuario y pass: ',username, password)
        try:
            user = Estudian.objects.get(username=username)
            #print('Inicio sesion: ', str(user))
            if user.check_password(password):
                # Las credenciales son válidas
                login(request, user, backend='inscrip.backends.EstudianBackend')
                request.session['usuario_id'] = user.id
                #print('El usuario es: ', user.id)
                return redirect('inscrip:mis_cursos')
            else:
                # Las credenciales son inválidas
                print('Las credenciales son inválidas')
                messages.error(request, 'Usuario o contraseña incorrectos.')
                return render(request, 'inicio_sesionEst.html')
        except Estudian.DoesNotExist:
            # El usuario no existe
            print('EL usuario no existe bro')
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'inicio_sesionEst.html')
    else:
        #print('no es post')
        return render(request, 'inicio_sesionEst.html')


def mis_cursos(request):
    usuario_id = request.session.get('usuario_id')
    periodo = settings.PERIODO
    anio = settings.ANIO
    estudiante = get_object_or_404(Estudian, id=usuario_id)
    #valor de aeta
    if estudiante.aeta is False:
        return redirect('inscrip:est_sin_aeta')

    if not usuario_id:
        return redirect('inscrip:inicio_sesionE')

    try:
        estudiante.incrementar_cont_veces()
        if estudiante.cont_final >= 5: # cambiar de 5 a1
            return redirect('inscrip:inicio_sesionE')
    except Estudian.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
        return redirect('inscrip:inicio_sesionE')

    #recuperar datos del estudiate
    cve_program = estudiante.cve_program
    if cve_program == 'ECD':
        cve_program = 'EST'

    cve_estud = estudiante.cve_estud
    programa = get_object_or_404(Coordinaciones, cve_program=cve_program)

    beca = Becarios.objects.filter(cve_estud=cve_estud).first()
    if beca is None:
        entidad_beca = ''
    else:
        entidad_beca = Catabeca.objects.filter(cve_becaria=beca.cve_becaria).first()

    # Filtra los registros de la tabla Estudiante_Consejero donde el campo cve_estud coincida con el valor de cve_estud.
    consejero_estudiante = estudiante_consejero.objects.filter(cve_estud=cve_estud).first()
    # Filtra los registros de la tabla Academic donde el campo cve_academic coincida con el valor de cve_academic.
    consejero = Academic.objects.filter(cve_academic=consejero_estudiante.cve_academic).first()

    # recuperar los cursos del estudiante

    capcursos =  Sinsevi.objects.filter(cve_estud=cve_estud) # se envia el objeto a html

    #nacionalidad
    pais ='MEXICANA'

    render_data = {
        'estudiante': estudiante, 'programa': programa, 'capcursos': capcursos, 'periodo': periodo, 'anio': anio, 'consejero': consejero,
        'entidad_beca': entidad_beca, 'pais': pais }

    return render(request, 'mis_cursos.html', render_data)

def est_sin_aeta(request):
    usuario_id = request.session.get('usuario_id')
    estudiante = get_object_or_404(Estudian, id=usuario_id)
    programa = get_object_or_404(Coordinaciones, cve_program=estudiante.cve_program)
    return render(request, 'est_sin_aeta.html', {'estudiante':estudiante, 'programa': programa})


def curso_to_dict(curso):
    return {
        'id': curso.id,
        'cve_program': curso.cve_program,
        'nombre': curso.nombre,
        'nom_academic': curso.nom_academic,
        'apellidos': curso.apellidos,
        'participacion': curso.participacion,
        'creditos': curso.creditos,
        'aula': curso.aula,
        'observaciones': curso.observaciones,
        'cve_academic': curso.cve_academic_id,
        'cve_curso': curso.cve_curso_id,
        'lunes_ini': curso.lunes_ini.strftime('%H:%M:%S') if curso.lunes_ini else None,
        'lunes_fin': curso.lunes_fin.strftime('%H:%M:%S') if curso.lunes_fin else None,
        'martes_ini': curso.martes_ini.strftime('%H:%M:%S') if curso.martes_ini else None,
        'martes_fin': curso.martes_fin.strftime('%H:%M:%S') if curso.martes_fin else None,
        'miercoles_ini': curso.miercoles_ini.strftime('%H:%M:%S') if curso.miercoles_ini else None,
        'miercoles_fin': curso.miercoles_fin.strftime('%H:%M:%S') if curso.miercoles_fin else None,
        'jueves_ini': curso.jueves_ini.strftime('%H:%M:%S') if curso.jueves_ini else None,
        'jueves_fin': curso.jueves_fin.strftime('%H:%M:%S') if curso.jueves_fin else None,
        'viernes_ini': curso.viernes_ini.strftime('%H:%M:%S') if curso.viernes_ini else None,
        'viernes_fin': curso.viernes_fin.strftime('%H:%M:%S') if curso.viernes_fin else None,
        'periodo': curso.periodo,
        'agno': curso.agno,
        'lunes_inip': curso.lunes_inip.strftime('%H:%M:%S') if curso.lunes_inip else None,
        'lunes_finp': curso.lunes_finp.strftime('%H:%M:%S') if curso.lunes_finp else None,
        'martes_inip': curso.martes_inip.strftime('%H:%M:%S') if curso.martes_inip else None,
        'martes_finp': curso.martes_finp.strftime('%H:%M:%S') if curso.martes_finp else None,
        'miercoles_inip': curso.miercoles_inip.strftime('%H:%M:%S') if curso.miercoles_inip else None,
        'miercoles_finp': curso.miercoles_finp.strftime('%H:%M:%S') if curso.miercoles_finp else None,
        'jueves_inip': curso.jueves_inip.strftime('%H:%M:%S') if curso.jueves_inip else None,
        'jueves_finp': curso.jueves_finp.strftime('%H:%M:%S') if curso.jueves_finp else None,
        'viernes_inip': curso.viernes_inip.strftime('%H:%M:%S') if curso.viernes_inip else None,
        'viernes_finp': curso.viernes_finp.strftime('%H:%M:%S') if curso.viernes_finp else None,
        'aulap': curso.aulap,
        'observacionesp': str(curso.observacionesp)
    }

def selecciona_curso(request):
    # Obtener todos los registros de la tabla CAPCURS
    print('Se ha dado el click man')
    usuario_id = request.session.get('usuario_id')
    usuario = Estudian.objects.get(id=usuario_id)
    los_cursos = Capcurs.objects.all()
    loscursos = los_cursos.order_by('cve_curso')
    clave = ['AEC', 'BOT', 'COA', 'DES', 'ECO', 'EDA', 'ENT', 'EST', 'FIV', 'FIT', 'FOR', 'FRU', 'GAN', 'GEN', 'HID',
             'SEM']
    valor = ['AGROECOLOGÍA Y SUSTENTABILIDAD', 'BOTANICA', 'CÓMPUTO APLICADO', 'DESARROLLO RURAL', 'ECONOMÍA',
             'EDAFOLOGÍA', 'ENTOMOLOGÍA Y ACAROLOGIA', 'ESTADISTICA Y CIENCIA DE DATOS', 'FISIOLOGIA VEGETAL', 'FITOPATOLOGIA',
             'CIENCIAS FORESTALES', 'FRUTICULTURA', 'GANADERIA', 'GENETICA', 'HIDROCIENCIAS', 'PRODUCCIÓN DE SEMILLAS']

    programas = dict(zip(clave, valor))

    cursos_por_programa = {}
    for programa in programas:
        # Obtener los cursos que pertenecen al programa actual
        cursos = Capcurs.objects.filter(cve_program=programa).order_by('cve_curso')
        cursos_por_programa[programa] = [curso_to_dict(curso) for curso in cursos]
    cursos_por_programa_json = json.dumps(cursos_por_programa)

    return render(request, 'selecciona_curso.html', {
        'usuario': usuario,
        'loscursos': loscursos,
        'programas': programas,
        'cursos_por_programa_json': cursos_por_programa_json
    })


def buscar_curso(request):
    print('Lo estamos haciendo')
    cve_curso = request.GET.get('cve_curso')
    cve_academic = request.GET.get('cve_academic')
    try:
        #elcurso = Capcurs.objects.filter(id=id_curso, cve_curso=cve_curso).first()
        #############
        # Suponiendo que tienes los valores seleccionados en las siguientes variables:
        selected_cve_curso = cve_curso  # Reemplaza esto con el valor seleccionado del campo cve_curso
        selected_cve_academic = cve_academic  # Reemplaza esto con el valor seleccionado del campo id_curso
        print('IDcurso y cve_curso es: ',selected_cve_academic,selected_cve_curso)

        # Filtrar los cursos que coinciden con el cve_curso seleccionado
        cursos_coincidentes = Capcurs.objects.filter(cve_curso=selected_cve_curso)
        for i in cursos_coincidentes:
            print(i.cve_academic_id)

        # Ahora, filtra dentro de los cursos coincidentes para obtener el curso con el id_curso seleccionado
        elcurso = cursos_coincidentes.filter(cve_academic=selected_cve_academic).first()

        # Si elcurso es None, significa que no se encontró un curso con el id_curso seleccionado,
        # por lo que puedes tomar simplemente el primer curso que coincide con el cve_curso
        if not elcurso:
            elcurso = cursos_coincidentes.first()

        # Ahora, elcurso contiene el objeto Capcurs correcto según la selección del usuario
        #################
        print('EL curso de la consulta es: ',elcurso.cve_curso_id, elcurso.cve_academic_id)
        if elcurso is not None:
            data = {
                'id_curso': elcurso.id,
                'cve_academic': elcurso.cve_academic_id,
                'nom_academic': elcurso.nom_academic,
                'apellidos': elcurso.apellidos,
                'participacion': elcurso.participacion,
                'creditos': elcurso.creditos,
                'aula': elcurso.aula,
                'observaciones': elcurso.observaciones,
                'lunes_ini': elcurso.lunes_ini,
                'lunes_fin': elcurso.lunes_fin,
                'martes_ini': elcurso.martes_ini,
                'martes_fin': elcurso.martes_fin,
                'miercoles_ini': elcurso.miercoles_ini,
                'miercoles_fin': elcurso.miercoles_fin,
                'jueves_ini': elcurso.jueves_ini,
                'jueves_fin': elcurso.jueves_fin,
                'viernes_ini': elcurso.viernes_ini,
                'viernes_fin': elcurso.viernes_fin,
                'periodo': elcurso.periodo,
                'agno': elcurso.agno,
                'lunes_inip': elcurso.lunes_inip,
                'lunes_finp': elcurso.lunes_finp,
                'martes_inip': elcurso.martes_inip,
                'martes_finp': elcurso.martes_finp,
                'miercoles_inip': elcurso.miercoles_inip,
                'miercoles_finp': elcurso.miercoles_finp,
                'jueves_inip': elcurso.jueves_inip,
                'jueves_finp': elcurso.jueves_finp,
                'viernes_inip': elcurso.viernes_inip,
                'viernes_finp': elcurso.viernes_finp,
                'aulap': elcurso.aulap,
                'observacionesp': elcurso.observacionesp
            }
            #print('la data es: ', data)
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'No se encontró el curso seleccionado'})
    except Exception as e:
        print(str(e))
        return JsonResponse({'error': str(e)})

def hay_colaboradores(request, cve_curso):
    #print('Ya fuimos a buscar colabs')
    colaboradores = Imparegu.objects.filter(cve_curso=cve_curso, participa='COLABORADOR')
    data = []
    for colab in colaboradores:
        profesor = Academic.objects.filter(cve_academic=colab.cve_academic).first()
        data.append({
            'clave': profesor.cve_academic,
            'nombre': profesor.nombres,
            'apellido': profesor.apellidos,
        })
    return JsonResponse({'data': data})  # Devolver un objeto JSON con el campo 'data'


#funcion que agrega curso regular a asistirá y sisevi
def crea_asistira(request):
    usuario_id = request.session.get('usuario_id')
    usuario = Estudian.objects.get(id=usuario_id)

    if request.method == 'POST':
        form_asistira = AsistiraForm(request.POST)
        form_sinsevi = SinseviForm(request.POST)

        if form_asistira.is_valid() and form_sinsevi.is_valid():
            cve_curso = request.POST.get('cve_curso', None)
            cve_academic = request.POST.get('cve_academic', None)
            id_curso = request.POST.get('id_curso', None)

            # Verificar si ya existe un registro con el mismo cve_curso y cve_estud
            asistira_existente = Asistira.objects.filter(cve_curso=cve_curso, cve_estud=usuario.cve_estud).first()
            if asistira_existente:
                return JsonResponse({'success': False, 'error': 'Ya agregaste este curso'})

            else:
                try:
                    # Intentar obtener el curso seleccionado con la combinación de id_curso y cve_academic
                    micurso = Capcurs.objects.get(id=id_curso, cve_curso=cve_curso, cve_academic=cve_academic)

                    print('De capcurs: ->', micurso.id, micurso.cve_curso_id, micurso.cve_academic_id)
                    catacurs = Catacurs.objects.get(cve_curso=cve_curso)

                    asistira = form_asistira.save(commit=False)
                    asistira.cve_estud = usuario.cve_estud
                    asistira.cve_curso = cve_curso
                    asistira.cve_academic = cve_academic
                    asistira.gpo_670 = catacurs.gpo_670
                    asistira.califica = 0
                    asistira.creditos = micurso.creditos
                    asistira.periodo = 'OTONO'
                    asistira.agno = micurso.agno
                    asistira.observa = 'PEND.'
                    asistira.registro = '1753-01-01'
                    asistira.per_vi_cur = catacurs.periodo
                    asistira.ano_vi_cur = catacurs.agno
                    asistira.no_periodo = 3
                    asistira.isevaluated = 0
                    asistira.save()
                    # asistiré creado

                    # Crea una instancia de Sinsevi y asigna el Capcurs
                    sinsevi = Sinsevi()
                    sinsevi.cve_estud = usuario.cve_estud
                    sinsevi.id_capcurs = micurso
                    sinsevi.cve_curso = cve_curso
                    sinsevi.nombre = micurso.nombre
                    sinsevi.cve_academic = cve_academic
                    sinsevi.nom_academic = micurso.nom_academic
                    sinsevi.apellidos = micurso.apellidos
                    sinsevi.gpo_670 = catacurs.gpo_670
                    sinsevi.save()
                    # sinsevi creado

                    return JsonResponse({'success': True})

                except Capcurs.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'El curso seleccionado no existe'})
        else:
            print(form_asistira.errors)
            print(form_sinsevi.errors)
            return JsonResponse({'success': False, 'error': 'Error en el formulario'})

    else:
        form_asistira = AsistiraForm()
        form_sinsevi =SinseviForm()

    return JsonResponse({'success': True})

# rodriguez.rosales@colpos.mx

#funcion que agrega INVESTIGACION
def crea_asistira690(request):
    # Obtener el ID de usuario de la sesión
    usuario_id = request.session.get('usuario_id')

    try:
        # Obtener el usuario
        usuario = Estudian.objects.get(id=usuario_id)
        print('El usuario: ', usuario.cve_estud)

        # Calcular el código del curso
        codigo_690 = usuario.cve_program + '690'

        # Verificar si el curso ya existe en la tabla Asistira
        if Asistira.objects.filter(cve_estud=usuario.cve_estud, cve_curso=codigo_690).exists():
            # El curso ya existe, enviar un mensaje de error.
            response_data = {'success': False, 'message': 'INVESTIGACIÓN ya ha sido agregado.'}
        else:
            # El curso no existe, crearlo.
            # Obtener datos del curso en Catacurs
            catacurs = Catacurs.objects.filter(cve_curso=codigo_690).first()
            print('Este es el curso: ', catacurs.cve_curso)

            if catacurs is None:
                # Manejar el caso en que no se encuentre el curso en Catacurs
                response_data = {'success': False, 'message': 'Curso no encontrado en Catacurs.'}
            else:
                # Obtener datos del investigador
                consejero_estudiante = estudiante_consejero.objects.filter(cve_estud=usuario.cve_estud).first()
                investigador = Imparegu.objects.filter(cve_curso=codigo_690, cve_academic=consejero_estudiante.cve_academic).first()
                print('EL profe es: ', investigador.cve_academic)

                if investigador is None:
                    # Manejar el caso en que no se encuentre el investigador
                    response_data = {'success': False, 'message': 'Investigador no encontrado.'}
                else:
                    print('La creacion de estos registros')
                    # Crear registro Asistira nuevo
                    asistira = Asistira.objects.create(
                        cve_estud=usuario.cve_estud,
                        cve_curso=codigo_690,
                        gpo_670=investigador.gpo_670,
                        califica=0,
                        creditos=9,
                        periodo='OTONO',
                        agno=2023,
                        observa='PEND.',  # valor por defecto
                        registro='1753-01-01',
                        per_vi_cur=catacurs.periodo,
                        ano_vi_cur=catacurs.agno,
                        no_periodo=3,  # valor por defecto primavera = 1 verano y otoño: 2,3
                        isevaluated=0  # cambiara a 1 cuando se haya evaluado
                    )

                    # Obtener datos del profesor
                    profesor = Academic.objects.filter(cve_academic=investigador.cve_academic).first()

                    # Crear registro Sinsevi
                    sinsevi = Sinsevi.objects.create(
                        cve_estud=usuario.cve_estud,
                        cve_curso=codigo_690,
                        nombre=catacurs.nombre,
                        cve_academic=investigador.cve_academic,
                        nom_academic=profesor.nombres,
                        apellidos=profesor.apellidos,
                        gpo_670=investigador.gpo_670,
                    )
                    # Agregar mensaje de éxito
                    response_data = {'success': True, 'message': 'INVESTIGACIÓN se ha agregado exitosamente.'}
    except Estudian.DoesNotExist:
        # Manejar el caso en que el usuario no existe
        response_data = {'success': False, 'message': 'Usuario no encontrado.'}
    return JsonResponse(response_data)


def elimina_uncurso(request, id_sinsevi):
    usuario_id = request.session.get('usuario_id')
    estudiante = Estudian.objects.get(id=usuario_id)
    print('se ha dado click a eliminar id: ', id_sinsevi)
    elcurso = Sinsevi.objects.filter(id_sinsevi=id_sinsevi).first()

    asistira = Asistira.objects.get(cve_estud=estudiante.cve_estud, cve_curso=elcurso.cve_curso)

    print('Tonces eliminar: ', asistira.cve_curso)
    # El curso no se encontró en capcurs, enviar mensaje de error

    sinsevi_instance = Sinsevi.objects.get(id_sinsevi=id_sinsevi)
    sinsevi_instance.delete()
    asistira.delete()  # Elimina todos los registros de la tabla asistira
    messages.success(request, 'Curso eliminado satisfactoriamente')

    return redirect('inscrip:mis_cursos')

def elimina_inv_690(request, id_curso):
    usuario_id = request.session.get('usuario_id')
    estudiante = Estudian.objects.get(id=usuario_id)
    cve_program = estudiante.cve_program
    cve_estud = estudiante.cve_estud
    programa = get_object_or_404(Coordinaciones, cve_program=cve_program)

    consejero_estudiante = estudiante_consejero.objects.filter(cve_estud=cve_estud).first()

    asistira = Asistira.objects.get(id=id_curso)  # obtengo el curso en asistira
    print('Tonces eliminar: ', asistira.cve_curso)
    # El curso no se encontró en capcurs, enviar mensaje de error
    asistira.delete()  # Elimina todos los registros de la tabla asistira
    messages.success(request, 'Curso eliminado satisfactoriamente')
    return redirect('inscrip:mis_cursos')


def guardar_boleta(request):
    usuario_id = request.session.get('usuario_id')
    periodo = settings.PERIODO
    anio = settings.ANIO
    estudiante = get_object_or_404(Estudian, id=usuario_id)
    #valor de aeta
    if estudiante.aeta is False:
        return redirect('inscrip:est_sin_aeta')

    if not usuario_id:
        return redirect('inscrip:inicio_sesionE')

    try:
        estudiante.incrementar_cont_veces()
        if estudiante.cont_final >= 5:
            return redirect('inscrip:inicio_sesionE')
    except Estudian.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
        return redirect('inscrip:inicio_sesionE')

    #recuperar datos del estudiate
    cve_program = estudiante.cve_program
    if cve_program == 'ECD':
        cve_program = 'EST'

    cve_estud = estudiante.cve_estud
    programa = get_object_or_404(Coordinaciones, cve_program=cve_program)

    beca = Becarios.objects.filter(cve_estud=cve_estud).first()
    if beca is None:
        entidad_beca = ''
    else:
        entidad_beca = Catabeca.objects.filter(cve_becaria=beca.cve_becaria).first()

    # Filtra los registros de la tabla Estudiante_Consejero donde el campo cve_estud coincida con el valor de cve_estud.
    consejero_estudiante = estudiante_consejero.objects.filter(cve_estud=cve_estud).first()
    # Filtra los registros de la tabla Academic donde el campo cve_academic coincida con el valor de cve_academic.
    consejero = Academic.objects.filter(cve_academic=consejero_estudiante.cve_academic).first()

    # recuperar los cursos del estudiante

    capcursos =  Sinsevi.objects.filter(cve_estud=cve_estud) # se envia el objeto a html

    #nacionalidad
    pais ='MEXICANA'

    render_data = {
        'estudiante': estudiante, 'programa': programa, 'capcursos': capcursos, 'periodo': periodo, 'anio': anio, 'consejero': consejero,
        'entidad_beca': entidad_beca, 'pais': pais }

    return render(request, 'guardar_boleta.html', render_data)


def recibir_archivo(request):
    if request.method == "POST" and request.FILES:
        print('si es post este arch')
        archivo = request.FILES["archivo"]
        nombre_archivo = archivo.name

        # Ruta donde se almacenarán los archivos (directorio 'AETA_2023' en el directorio de medios de Django)
        ruta_archivos = os.path.join("AETA_2023", nombre_archivo)

        # Guardar el archivo en el servidor
        with open(ruta_archivos, "wb") as destino:
            for chunk in archivo.chunks():
                destino.write(chunk)

        # Aquí puedes realizar otras operaciones con el archivo si es necesario

        return JsonResponse({"message": "El archivo se ha guardado correctamente."})

    return JsonResponse({"message": "No se ha recibido ningún archivo o el método de solicitud no es válido."})


def cursos_asistire(request):
    usuario_id = request.session.get('usuario_id')
    periodo = settings.PERIODO
    anio = settings.ANIO
    estudiante = get_object_or_404(Estudian, id=usuario_id)
    # valor de aeta
    if estudiante.aeta is False:
        return redirect('inscrip:est_sin_aeta')

    if not usuario_id:
        return redirect('inscrip:inicio_sesionE')

    try:
        estudiante.incrementar_cont_veces()
        if estudiante.cont_final >= 5:
            return redirect('inscrip:inicio_sesionE')
    except Estudian.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
        return redirect('inscrip:inicio_sesionE')

    # recuperar datos del estudiate
    cve_program = estudiante.cve_program
    if cve_program == 'ECD':
        cve_program = 'EST'

    cve_estud = estudiante.cve_estud
    programa = get_object_or_404(Coordinaciones, cve_program=cve_program)

    beca = Becarios.objects.filter(cve_estud=cve_estud).first()
    if beca is None:
        entidad_beca = ''
    else:
        entidad_beca = Catabeca.objects.filter(cve_becaria=beca.cve_becaria).first()

    # Filtra los registros de la tabla Estudiante_Consejero donde el campo cve_estud coincida con el valor de cve_estud.
    consejero_estudiante = estudiante_consejero.objects.filter(cve_estud=cve_estud).first()
    # Filtra los registros de la tabla Academic donde el campo cve_academic coincida con el valor de cve_academic.
    consejero = Academic.objects.filter(cve_academic=consejero_estudiante.cve_academic).first()

    # recuperar los cursos del estudiante

    capcursos = Sinsevi.objects.filter(cve_estud=cve_estud)  # se envia el objeto a html

    # nacionalidad
    pais = 'MEXICANA'

    render_data = {
        'estudiante': estudiante, 'programa': programa, 'capcursos': capcursos, 'periodo': periodo, 'anio': anio,
        'consejero': consejero,
        'entidad_beca': entidad_beca, 'pais': pais}

    return render(request, 'cursos_asistire.html', render_data)


# IMplementacion de envio de pdf
def generarPDF(request):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        estudiante = get_object_or_404(Estudian, id=usuario_id)

        consejero_estudiante = estudiante_consejero.objects.filter(cve_estud=estudiante.cve_estud).first()
        consejero = Academic.objects.filter(cve_academic=consejero_estudiante.cve_academic).first()
        if estudiante.cve_program == 'ECD':
            estudiante.cve_program = 'EST'

        coordinacion = Coordinaciones.objects.filter(cve_program=estudiante.cve_program).first()

        archivo_adjunto = request.FILES.get('pdf')
        # Envía el correo electrónico
        destinatario = ['sistema.inscripcioncm@colpos.mx', estudiante.username]
        #destinatario = ['sinscripcolpos@gmail.com', estudiante.e_mailcp, 'servacadmontecillo@colpos.mx', consejero.email, coordinacion.username, 'posgradosybecas@colpos.mx']
        print(estudiante.nombres)
        asunto = 'Boleta de preinscripción' + ' ' + str(estudiante.cve_estud) + ' ' + estudiante.nombres + ' ' + estudiante.apellidos
        periodo = settings.PERIODO
        mensaje = 'C O L E G I O   D E   P O S T G R A D U A D O S\n'
        mensaje += 'C A M P U S   M O N T E C I L L O\n\n'
        mensaje += 'Se adjunta documento PDF de la boleta de preinscripción para el periodo de ' + periodo +  ' del estudiante '  + estudiante.cve_program + '-' + str(estudiante.cve_estud) + '-'+ estudiante.nombres + ' ' + estudiante.apellidos
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

        #crear nombre del archivo
        nombre_archivo = f'{estudiante.cve_program}-{estudiante.cve_estud}-{estudiante.nombres}_{estudiante.apellidos}-{settings.PERIODO}_{settings.ANIO}.pdf'
        archivo_adjunto.name = nombre_archivo

        # Adjuntar el archivo PDF al correo electrónico
        email.attach(archivo_adjunto.name, archivo_adjunto.read(), 'application/pdf')

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
            estudiante = Estudian.objects.get(id=estudiante.id)
            estudiante.incrementar_cont_final()
            messages.success(request, '¡Correo electrónico enviado correctamente!')
            # Redirige a la página 'cursos_guardados'
            return redirect('inscrip:cursos_asistire')
        except smtplib.SMTPException as e:
            messages.success(request, '¡Correo electrónico no enviado, intente de nuevo!')
            return HttpResponse(f'Error al enviar el correo electrónico: {str(e)}')
    return HttpResponse('Error al generar el PDF')
