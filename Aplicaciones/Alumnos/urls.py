from django.urls import path
from . import views

urlpatterns = [
    path('',views.inicio),
    path('CrearAlumno',views.nuevoalumno, name='CrearAlumno'),
    path('AgregarAlumno',views.guardaralumno, name='AgregarAlumno'),
    path('ListadoAlumno',views.listadoAlumno, name='ListadoAlumno'),
    path('EliminarAlumno/<int:id>/',views.eliminaralumno, name='EliminarAlumno'),
    path('EditarAlumno/<int:id>/',views.editaralumno, name='EditarAlumno'),
    path('CrearProfesor',views.nuevoprofesor, name='CrearProfesor'),
    path('AgregarProfesor',views.guardarprofesor, name='AgregarProfesor'),
    path('ListadoProfesor',views.listadoProfesor, name='ListadoProfesor'),
    path('EliminarProfesor/<int:id>/',views.eliminarprofesor, name='EliminarProfesor'),
    path('EditarProfesor/<int:id>/',views.editarprofesor, name='EditarProfesor'),
    path('CrearCurso',views.nuevocurso, name='CrearCurso'),
    path('AgregarCurso',views.guardarcurso, name='AgregarCurso'),
    path('buscar_estudiantes/', views.buscar_estudiantes, name='buscar_estudiantes'),
    path('ListadoCurso',views.listadocurso, name='ListadoCurso'),
    path('EliminarCurso/<int:id>/',views.eliminarcurso, name='EliminarCurso'),
    path('EditarCurso/<int:id>/',views.editarcurso, name='EditarCurso'),
    path('TomarAsistencia/<int:id>/',views.tomarAsistencia, name='TomarAsistencia'),
    path('InformeAsistencias/<int:id>/', views.informeAsistencias, name='InformeAsistencias'),
    path('InformeAsistencias/<int:id>/eliminar/', views.eliminar_informe_asistencias, name='eliminar_informe_asistencias'),
    path('RegistrarNotas/<int:id>/', views.registrarnotas, name='RegistrarNotas'),
    path('InformeNotas/<int:id>/', views.informeNotas, name='InformeNotas'),
    path('InformeNotas/<int:id>/eliminar/', views.eliminar_informe, name='eliminar_informe'),


]
