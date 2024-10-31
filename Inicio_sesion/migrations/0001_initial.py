
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=100)),
                ('foundationDate', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('NIT', models.CharField(default='1111111111', max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('country', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('identification', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('nationality', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('birthday', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('position', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('is_entrepreneur', models.BooleanField(default=False)),
                ('entrepreneurship', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(max_length=128)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inicio_sesion.company')),
            ],
        ),
    ]
