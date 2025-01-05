from django.db import models
import uuid
# Create your models here.

class Docente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cedula = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    matricula = models.CharField(max_length=20, unique=True, editable=False)
    cedula = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        if not self.matricula:
            self.matricula = str(uuid.uuid4())[:8].upper()  # Genera una matrícula única
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.matricula})"

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, related_name='cursos')
    estudiantes = models.ManyToManyField(Estudiante, related_name='cursos')

    def __str__(self):
        return self.nombre


class Asistencia(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha = models.DateField()
    presente = models.BooleanField(default=False)

    class Meta:
        unique_together = ('estudiante', 'curso', 'fecha')

    def __str__(self):
        return f"Asistencia {self.estudiante.nombre} - {self.fecha}"


class Calificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    evaluacion = models.CharField(max_length=100)  # Ej: "Parcial 1", "Tarea 2"
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Calificación {self.estudiante.nombre} - {self.evaluacion}: {self.calificacion}"
