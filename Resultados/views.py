from django.shortcuts import render

from django.db import models
import json
from sqlite3 import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from Inicio_sesion.models import CustomUser, Company
from Formulario.models import Form, Section, FormSection, Response
from django.contrib.auth.models import User
from Resultados.models import ResultadosUsuario, ResultadosEmpresa

def index(request):
    """
    Muestra el inicio de la plataforma con el login en ingles
    """
    return HttpResponse("This is an index page")


def resultadosUsuarios(request):
    """
    View for userView.html
    """
    # Obtén el correo electrónico de la sesión
    email = request.session.get("user_email")
    if email:
        # Obten informacion del usuario
        user_info = CustomUser.objects.get(email=email)   
        # print(user_info)     
        # Convertir la información del usuario en un diccionario para poder pasarla a la plantilla
        
        # Unanswered forms
        # Obtener todas las respuestas asociadas al usuario
        responses = Response.objects.filter(employee=user_info)

        #obtener todas las respuestas que dio el usuario, con id de pregunta, id del formulario y la respuesta
        answers = responses.values_list('question', 'form', 'answer')
        # Si hay varios formularios, dividir las respuestas por formulario
        forms = {}
        for answer in answers:
            question_id, form_id, answer = answer
            if form_id not in forms:
                forms[form_id] = []
            forms[form_id].append((question_id, answer))

        # print(forms)

        # vectores de valor
        valorVectorDesemContex = [0.0834,0.1045,0.1301,0.1524,0.175,0.1223,0.1272,0.1048]
        valorVectorDesemContra = [0.1882,0.2051,0.2252,0.2039,0.1774]
        valorVectorDesemTarea = [0.238,0.327,0.271,0.162]
        estrateAutoLide = [31.72,31.55,36.72]
        valorVectorEstraComp = [20.03,19.18,13.06,12.4,1.37,0.2,14.66,8.67,10.36]
        valorVectorPensaConstru = [18.46,6.41,13.57,22.67,19.03,10.91,8.92]
        valorVectorRecomNatu = [27.21,37.26,35.51]
        estrateDesem = [0.4817,0.3936,0.1246]
        valorVectorApoOrgAOP1 = 17.31*0.01
        valorVectorApoOrgAOP2 = 19.63*0.01
        valorVectorApoOrgAOP3 = 19.83*0.01
        valorVectorApoOrgAOP4 = 17.43*0.01
        valorVectorApoOrgAOP5 = 16.7*0.01
        valorVectorApoOrgAOP6 = 9.08*0.01
        # valorVectorApoOrgTaop = []
        resultados = {}
        # Multiplicar los question_id del 1 al 8 con los valores del vector y sumarlos, pero cada resultado asociado solo con su form_id
        for form_id, answers in forms.items():
            total = [0]*15
            for question_id, answer in answers:
                if question_id >= 1 and question_id <= 8:
                    total[0] += answer * valorVectorDesemContex[question_id-1]
                elif question_id >= 9 and question_id <= 13:
                    total[1] += answer * valorVectorDesemContra[question_id-9]
                elif question_id >= 14 and question_id <= 17:
                    total[2] += answer * valorVectorDesemTarea[question_id-14]
                elif question_id >= 18 and question_id <= 26:
                    total[3] += answer * (valorVectorEstraComp[question_id-18]*0.01)
                elif question_id >= 27 and question_id <= 33:
                    total[4] += answer * (valorVectorPensaConstru[question_id-27]*0.01)
                elif question_id >= 34 and question_id <= 36:
                    total[5] += answer * (valorVectorRecomNatu[question_id-34]*0.01)
                elif question_id == 37:
                    total[6] += answer * valorVectorApoOrgAOP1
                elif question_id == 38:
                    total[7] += answer * valorVectorApoOrgAOP2
                elif question_id == 39:
                    total[8] += answer * valorVectorApoOrgAOP3
                elif question_id == 40:
                    total[9] += answer * valorVectorApoOrgAOP4
                elif question_id == 41:
                    total[10] += answer * valorVectorApoOrgAOP5
                elif question_id == 42:
                    total[11] += answer * valorVectorApoOrgAOP6
            #suma todos los valores de total
            total[12] = (estrateAutoLide[0]*0.01)*total[3]+(estrateAutoLide[1]*0.01)*total[5]+(estrateAutoLide[2]*0.01)*total[4]
            total[13] = estrateDesem[0]*total[2]+estrateDesem[1]*total[0]+estrateDesem[2]*total[1]
            total[14] = sum(total[6:12])
            #redondear a 2 decimales
            total = [round(i,2) for i in total]
            
            sesion = 0
            
            for resultadosSection in total:
                resultados_usuario = ResultadosUsuario.objects.create(
                id_empleado=user_info.id,
                id_empresa_empleado=user_info.company_id,
                id_formulario=form_id,
                evaluado_usu=sesion+1,
                resultado_usu=resultadosSection)
                sesion += 1

        return HttpResponse(str(resultados))

def resultadosEmpre(request):
    """
    View for userView.html
    """
    # Obtén el correo electrónico de la sesión
    email = request.session.get("user_email")

    if email:
        # Obten informacion del usuario
        user_info = Company.objects.get(email=email)
        empresa = user_info.id

        #Si en ResultadosEmpresa hay al menos un registro con el id de la empresa, borrarlo
        if ResultadosEmpresa.objects.filter(id_empresa=empresa).exists():
            ResultadosEmpresa.objects.filter(id_empresa=empresa).delete()

        # Obtener todas las respuestas asociadas a la empresa
        responses = ResultadosUsuario.objects.filter(id_empresa_empleado=empresa)        
        #obtener todas las respuestas que dio el usuario, con id de pregunta, id del formulario y la respuesta
        answers = responses.values_list('id_formulario', 'evaluado_usu', 'resultado_usu')

        # Si hay varios formularios, dividir las respuestas por formulario
        forms = {}
        for resultado_usu in answers:
            id_formulario, evaluado_usu, resultado_usu = resultado_usu
            if id_formulario not in forms:
                forms[id_formulario] = []
            forms[id_formulario].append((evaluado_usu, resultado_usu))

        # print(forms)
        for form in forms:
            multiplo = int(len(forms[form])/15)
            lista = list(forms[form])            
            #bucle de solo 15 veces
            for i in range(15):
                suma = 0
                for k in range(multiplo):
                    suma += lista[i+k*15][1]
                    # print(lista[i+k*15][1])                
                promedio = suma/multiplo
                promedio = round(promedio,3)
                # print(promedio)
                resultados_empresa = ResultadosEmpresa.objects.create(
                    id_empresa=empresa,
                    id_formulario_nombre=form,
                    evaluado_empre=i+1,
                    resultado_empre=promedio)
        return HttpResponse("Resultados guardados")