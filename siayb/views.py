from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login

from SINSCRIP import settings
from capcursapp.models import Academic
from inscrip.models import Estudian, Coordinaciones, Becarios, Catabeca, estudiante_consejero, Sinsevi


# Create your views here.
def inicio_siayb(request):
    # Cerrar sesión (antes de redireccionar)
    return render(request, 'inicio_sesionsiayb.html')


def logout_view(request):
    logout(request)
    return redirect('siayb:inicio_siayb')



def verificar_credenciale_siayb(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('usuario y pass: ',username, password)
        try:
            user = Estudian.objects.get(username=username)
            print('Inicio sesion: ', str(user))
            if user.check_password(password):
                # Las credenciales son válidas
                login(request, user, backend='inscrip.backends.EstudianBackend')
                request.session['usuario_id'] = user.id
                print('El usuario es valido: ', user.id)
                return redirect('siayb:mis_cursos_siayb')
            else:
                # Las credenciales son inválidas
                print('Las credenciales son inválidas')
                messages.error(request, 'Usuario o contraseña incorrectos.')
                return render(request, 'inicio_sesionsiayb.html')
        except Estudian.DoesNotExist:
            # El usuario no existe
            print('EL usuario no existe bro')
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'inicio_sesionsiayb.html')
    else:
        print('no es post')
        return render(request, 'inicio_sesionsiayb.html')


def mis_cursos_siayb(request):

    usuario_id = request.session.get('usuario_id')
    periodo = settings.PERIODO
    anio = settings.ANIO
    estudiante = get_object_or_404(Estudian, id=usuario_id)
    #valor de aeta
    print(' Entro el usuario: ', estudiante.cve_estud)
    if estudiante.aeta is False:
        print('Sin acta man')
        return redirect('inscrip:est_sin_aeta')

    if not usuario_id:
        return redirect('inscrip:inicio_sesionE')

    try:
        estudiante.incrementar_cont_veces()
        if estudiante.cont_final >= 5: # cambiar de 5 a1
            return redirect('siayb:inicio_siayb')
    except Estudian.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
        return redirect('siayb:inicio_siayb')

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
    print('Enviamos la info senior')

    render_data = {
        'estudiante': estudiante, 'programa': programa, 'capcursos': capcursos, 'periodo': periodo, 'anio': anio, 'consejero': consejero,
        'entidad_beca': entidad_beca, 'pais': pais }

    return render(request, 'mis_cursos_siayb.html', render_data)