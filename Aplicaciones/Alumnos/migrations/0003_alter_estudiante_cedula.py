# Generated by Django 4.0.6 on 2025-01-03 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alumnos', '0002_estudiante_cedula_alter_estudiante_matricula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='cedula',
            field=models.CharField(max_length=15),
        ),
    ]
