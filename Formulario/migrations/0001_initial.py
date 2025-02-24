# Generated by Django 5.0.3 on 2024-06-10 21:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Inicio_sesion', '0002_alter_company_nit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('authorized_employees', models.ManyToManyField(related_name='authorized_forms', to='Inicio_sesion.customuser')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inicio_sesion.company')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='Formulario.section')),
            ],
        ),
        migrations.CreateModel(
            name='FormSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_sections', to='Formulario.form')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections_form', to='Formulario.section')),
            ],
        ),
        migrations.AddField(
            model_name='form',
            name='sections',
            field=models.ManyToManyField(related_name='forms', through='Formulario.FormSection', to='Formulario.section'),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.IntegerField(choices=[(1, 'No lo describe nada'), (2, 'No le describe bien'), (3, 'Lo describe de cierta manera'), (4, 'Lo describe bien'), (5, 'Lo describe muy bien')])),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='Inicio_sesion.customuser')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='Formulario.form')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='Formulario.question')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='Formulario.section')),
            ],
            options={
                'unique_together': {('employee', 'form', 'section', 'question')},
            },
        ),
    ]
