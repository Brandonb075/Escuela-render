from django.shortcuts import *
from django.utils.dateparse import parse_date
from .models import *
from django.db.utils import *
from django.core.exceptions import *
from django.utils import *
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

###########################################################################################################
# Presentación en pantalla del formulario de nuevo estudiante
def nuevoalumno(request):
    return render(request, 'crearalumnos.html')

# Listar Alumnos
def listadoAlumno(request):
    alumnos = Estudiante.objects.all()
    return render(request, 'listaralumnos.html', {'alumnos': alumnos})

# Guardar los datos de estudiante
def guardaralumno(request):
    if request.method == 'POST':
        nombre = request.POST.get('txt_nombre')
        cedula = request.POST.get('txt_cedula')
        email = request.POST.get('txt_email')

        try:
            # Crear y guardar el estudiante (matrícula generada automáticamente)
            Estudiante.objects.create(
                nombre=nombre,
                cedula=cedula,
                email=email
            )
            print("Alumno creado exitosamente")
        except IntegrityError as e:
            error_message = "Error al guardar estudiante: La cédula ingresada ya existe."
            return render(request, 'crearalumnos.html', {
                'error_message': error_message,
                'nombre': nombre,
                'cedula': cedula,
                'email': email
            })
        except Exception as e:
            error_message = f"Error inesperado: {e}"
            return render(request, 'crearalumnos.html', {
                'error_message': error_message,
                'nombre': nombre,
                'cedula': cedula,
                'email': email
            })

        # Redirigir al listado de alumnos
        return redirect('ListadoAlumno')

#Editar Alumno
def editaralumno(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    if request.method == 'POST':
        estudiante.nombre = request.POST['txt_nombre']
        estudiante.cedula = request.POST['txt_cedula']
        estudiante.email = request.POST['txt_email']
        estudiante.save()
        return redirect('ListadoAlumno')
    return render(request, 'editaralumnos.html', {'estudiante': estudiante})

#Eliminar Alumno
def eliminaralumno(request, id):
    genero = get_object_or_404(Estudiante, id=id)
    genero.delete()
    return redirect('ListadoAlumno')




###########################################################################################################
# Presentación en pantalla del formulario de nuevo Profesor
def nuevoprofesor(request):
    return render(request, 'crearprofesor.html')

# Listar Profesor
def listadoProfesor(request):
    profesores = Docente.objects.all()
    return render(request, 'listarprofesor.html', {'profesores': profesores})

# Guardar los datos de Profesor
def guardarprofesor(request):
    if request.method == 'POST':
        nombre = request.POST.get('txt_nombre')
        cedula = request.POST.get('txt_cedula')
        email = request.POST.get('txt_email')

        try:
            # Crear y guardar el Profesor 
            Docente.objects.create(
                nombre=nombre,
                cedula=cedula,
                email=email
            )
            print("Profesor creado exitosamente")
        except IntegrityError as e:
            error_message = "Error al guardar Docente: La cédula ingresada ya existe."
            return render(request, 'crearProfesor.html', {
                'error_message': error_message,
                'nombre': nombre,
                'cedula': cedula,
                'email': email
            })
        except Exception as e:
            error_message = f"Error inesperado: {e}"
            return render(request, 'crearprofesor.html', {
                'error_message': error_message,
                'nombre': nombre,
                'cedula': cedula,
                'email': email
            })

        # Redirigir al listado de Profesor
        return redirect('ListadoProfesor')

#Editar Profesor
def editarprofesor(request, id):
    profesores = get_object_or_404(Docente, id=id)
    if request.method == 'POST':
        profesores.nombre = request.POST['txt_nombre']
        profesores.cedula = request.POST['txt_cedula']
        profesores.email = request.POST['txt_email']
        profesores.save()
        return redirect('ListadoProfesor')
    return render(request, 'editarprofesor.html', {'profesores': profesores})

#Eliminar Profesor
def eliminarprofesor(request, id):
    profesor = get_object_or_404(Docente, id=id)
    profesor.delete()
    return redirect('ListadoProfesor')



###########################################################################################################

# Presentar formulario de nuevo curso
def nuevocurso(request):
    docentes = Docente.objects.all()
    estudiantes = Estudiante.objects.all()

    query = request.GET.get('q', '')  # Obtén la cédula ingresada por el usuario
    if query:
        estudiantes = estudiantes.filter(cedula__icontains=query)  # Filtrar por cédula

    return render(request, 'crearcursos.html', {
        'docentes': docentes,
        'estudiantes': estudiantes,
        'query': query,  # Para mantener el valor en el campo de búsqueda
    })


# Listar todos los cursos
def listadocurso(request):
    cursos = Curso.objects.all()
    return render(request, 'listarcursos.html', {'cursos': cursos})

# Guardar nuevo curso
def guardarcurso(request):
    if request.method == 'POST':
        nombre = request.POST['txt_nombre']
        descripcion = request.POST['txt_descripcion']
        docente_id = request.POST['txt_docente']
        estudiantes_ids = request.POST.getlist('txt_estudiantes')

        # Guardar el curso en la base de datos
        try:
            docente = Docente.objects.get(id=docente_id)
            nuevo_curso = Curso.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                docente=docente,
            )

            # Asociar los estudiantes al curso
            for estudiante_id in estudiantes_ids:
                estudiante = Estudiante.objects.get(id=estudiante_id)
                nuevo_curso.estudiantes.add(estudiante)

            nuevo_curso.save()
            print("Curso creado correctamente")
        except Exception as e:
            print(f"Error al guardar curso: {e}")
            return render(request, 'crearcursos.html', {'error': str(e)})

        # Redirigir al listado de cursos
        return redirect('ListadoCurso')

    return redirect('nuevocurso')  # Si no es POST, redirige al formulario


#buscar estudiantes para generar el curso
def buscar_estudiantes(request):
    query = request.GET.get('q', '')
    if query:
        estudiantes = Estudiante.objects.filter(cedula__icontains=query)
    else:
        estudiantes = Estudiante.objects.all()

    # Serializar los resultados
    estudiantes_data = [
        {'id': estudiante.id, 'nombre': estudiante.nombre, 'cedula': estudiante.cedula}
        for estudiante in estudiantes
    ]
    return JsonResponse({'estudiantes': estudiantes_data})

# Editar curso
def editarcurso(request, id):
    curso = get_object_or_404(Curso, id=id)
    docentes = Docente.objects.all()
    estudiantes = Estudiante.objects.all()
    
    if request.method == 'POST':
        curso.nombre = request.POST['txt_nombre']
        curso.descripcion = request.POST['txt_descripcion']
        docente_id = request.POST['txt_docente']
        estudiantes_ids = request.POST.getlist('txt_estudiantes')

        # Actualizar docente
        docente = Docente.objects.get(id=docente_id)
        curso.docente = docente

        # Limpiar estudiantes anteriores y agregar los nuevos
        curso.estudiantes.clear()
        for estudiante_id in estudiantes_ids:
            estudiante = Estudiante.objects.get(id=estudiante_id)
            curso.estudiantes.add(estudiante)

        curso.save()
        return redirect('ListadoCurso')

    return render(request, 'editarcurso.html', {'curso': curso, 'docentes': docentes, 'estudiantes': estudiantes})

# Eliminar curso
def eliminarcurso(request, id):
    curso = get_object_or_404(Curso, id=id)
    curso.delete()
    return redirect('ListadoCurso')



######################################################################################################
# Asistencias
def tomarAsistencia(request, id):
    curso = get_object_or_404(Curso, id=id)
    estudiantes = curso.estudiantes.all()  # Obtener todos los estudiantes del curso

    if request.method == 'POST':
        fecha = request.POST['fecha']
        for estudiante in estudiantes:
            estado = request.POST.get(f'estado_{estudiante.id}')
            if estado:
                estado = True
            else:
                estado = False

            Asistencia.objects.update_or_create(
                estudiante=estudiante,
                curso=curso,
                fecha=fecha,
                defaults={'presente': estado}
            )

        return redirect('ListadoCurso')

    return render(request, 'tomarasistencia.html', {
        'curso': curso,
        'estudiantes': estudiantes,
    })


def informeAsistencias(request, id):
    curso = get_object_or_404(Curso, id=id)
    estudiantes = curso.estudiantes.all()

    if not estudiantes:
        print("No hay estudiantes asociados a este curso.")
        return render(request, 'informesasistencias.html', {'curso': curso, 'informe': []})

    informe = []

    for estudiante in estudiantes:
        asistencias = Asistencia.objects.filter(curso=curso, estudiante=estudiante)
        print(f"Asistencias para {estudiante.nombre}: {asistencias}")

        total_asistencias = asistencias.filter(presente=True).count()
        total_inasistencias = asistencias.filter(presente=False).count()
        total_registros = asistencias.count()

        if total_registros == 0:
            print(f"El estudiante {estudiante.nombre} no tiene registros de asistencia.")

        porcentaje_asistencia = (
            (total_asistencias / total_registros) * 100 if total_registros > 0 else 0
        )
        porcentaje_inasistencia = (
            (total_inasistencias / total_registros) * 100 if total_registros > 0 else 0
        )

        fechas_asistencias = asistencias.filter(presente=True).values_list('fecha', flat=True)
        fechas_inasistencias = asistencias.filter(presente=False).values_list('fecha', flat=True)

        informe.append({
            'estudiante': estudiante,
            'total_asistencias': total_asistencias,
            'total_inasistencias': total_inasistencias,
            'porcentaje_asistencia': porcentaje_asistencia,
            'porcentaje_inasistencia': porcentaje_inasistencia,
            'fechas_asistencias': fechas_asistencias,
            'fechas_inasistencias': fechas_inasistencias,
        })

    print(f"Informe generado: {informe}")
    return render(request, 'informesasistencias.html', {'curso': curso, 'informe': informe})


#eliminar informe asistenacias
def eliminar_informe_asistencias(request, id):
    try:
        curso = Curso.objects.get(id=id)
        # Eliminar todas las asistencias asociadas al curso
        curso.asistencia_set.all().delete()
        messages.success(request, f"El informe de asistencias del curso '{curso.nombre}' ha sido eliminado correctamente.")
    except Curso.DoesNotExist:
        messages.error(request, "El curso no existe.")
    
    return redirect('listado_informes')

########################################################################################################
#notas
#registrar notas
def registrarnotas(request, id):
    curso = get_object_or_404(Curso, id=id)
    estudiantes = curso.estudiantes.all()

    if request.method == 'POST':
        evaluacion = request.POST.get('evaluacion')  # El nombre del deber o evaluación

        for estudiante in estudiantes:
            calificacion = request.POST.get(f'calificacion_{estudiante.id}')  # La calificación de cada estudiante
            if calificacion:
                # Guardar o actualizar la calificación para el estudiante
                Calificacion.objects.update_or_create(
                    curso=curso,
                    estudiante=estudiante,
                    evaluacion=evaluacion,
                    defaults={'calificacion': calificacion}
                )
        return redirect('ListadoCurso')  # Redirigir al informe de calificaciones o página correspondiente

    return render(request, 'registrarnotas.html', {'curso': curso, 'estudiantes': estudiantes})
#informe Notas
def informeNotas(request, id):
    curso = get_object_or_404(Curso, id=id)
    estudiantes = curso.estudiantes.all()

    informe = []

    for estudiante in estudiantes:
        # Recupera todas las calificaciones del estudiante para el curso
        calificaciones = Calificacion.objects.filter(curso=curso, estudiante=estudiante)

        # Verifica que se están recuperando las calificaciones
        print(f"Calificaciones para {estudiante.nombre}: {calificaciones}")

        total_calificaciones = 0
        num_calificaciones = 0
        notas = []
        tareas = []

        # Recoge las calificaciones y tareas
        for calificacion in calificaciones:
            total_calificaciones += calificacion.calificacion
            num_calificaciones += 1
            notas.append(calificacion.calificacion)
            tareas.append(calificacion.evaluacion)

        if num_calificaciones > 0:
            promedio = total_calificaciones / num_calificaciones
        else:
            promedio = 0

        # Calcula el porcentaje basado en el promedio
        porcentaje = (promedio / 10) * 100

        # Verifica si es aprobado o desaprobado
        estado = "Aprobado" if porcentaje >= 70 else "Desaprobado"

        informe.append({
            'estudiante': estudiante,
            'calificaciones': zip(tareas, notas),  # Empareja las tareas con las notas
            'promedio': promedio,
            'porcentaje': porcentaje,
            'estado': estado
        })

    return render(request, 'informenotas.html', {'curso': curso, 'informe': informe})
#eliminar informe notas
def eliminar_informe(request, id):
    try:
        curso = Curso.objects.get(id=id)
        # Eliminar todas las calificaciones asociadas al curso
        curso.calificacion_set.all().delete()
        messages.success(request, f"El informe del curso '{curso.nombre}' ha sido eliminado correctamente.")
    except Curso.DoesNotExist:
        messages.error(request, "El curso no existe.")
    
    return redirect('ListadoCurso') 