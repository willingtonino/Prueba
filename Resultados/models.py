from django.db import models

class ResultadosUsuario(models.Model):
    id_resultado_usu = models.AutoField(primary_key=True)
    id_empleado = models.IntegerField()
    id_empresa_empleado = models.IntegerField()
    id_formulario = models.IntegerField()
    evaluado_usu = models.IntegerField() #Id Nombre de lo que se esta evaluando
    resultado_usu = models.FloatField()

class ResultadosEmpresa(models.Model):
    id_resultado_emp = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField()
    id_formulario_nombre = models.IntegerField()
    evaluado_empre = models.IntegerField()
    resultado_empre = models.FloatField()