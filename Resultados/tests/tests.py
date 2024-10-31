from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
# from ..models import CustomUser, Company, Form, Section, FormSection, Question, Response
from Formulario.models import Form, Section, FormSection, Question, Response
from Inicio_sesion.models import CustomUser, Company
from Resultados.models import ResultadosUsuario, ResultadosEmpresa

from django.contrib.auth.models import User
# from Formulario.models import Form, Section, FormSection, Question
import random


# Setup for the tests
class TestForm(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas
        self.signup_business_url = reverse('Inicio_sesion:signup_business')
        self.signup_user_url = reverse('Inicio_sesion:signup')
        self.create_form_url = reverse('Formulario:createForm')
        self.signin_url = reverse('Inicio_sesion:signin')
        self.user_view_url = reverse('Formulario:userView')
        self.resul_user_url = reverse('Resultados:resultadosUsuarios')
        self.resul_Empre_url = reverse('Resultados:resultadosEmpre')
        self.testCompany1 = {
            'companyName': 'Test Company 1',
            'dateFoundation': '2022-01-01',
            'email': 'test@company1.com',
            'NIT': '1234567890',
            'phone': '1234567890',
            'country': 'United States',
            'password': 'mypassword123'
        }
        self.testCompany2 = {
            'companyName': 'Test Company 2',
            'dateFoundation': '2023-01-01',
            'email': 'test@company2.com',  
            'NIT': '1234567891',
            'phone': '0987654321',
            'country': 'Canada',
            'password': 'mypassword456'
        }
        self.testEmployee1 = {
            'first_name': 'Test',
            'last_name': 'Employee 1',
            'identification': '1234567890',
            'gender': 'M',
            'nationality': 'United States',
            'country': 'United States',
            'birthday': '2000-01-01',
            'email': 'test@user1.com',
            'company': self.testCompany1['companyName'],
            'position': 'Supervisor',
            'phone': '1234567890',
            'is_entrepreneur': False,
            'entrepreneurship': '',
            'password': 'mypassword123'
        }
        self.testEmployee2 = {
            'first_name': 'Test',
            'last_name': 'Employee 2',
            'identification': '0987654321',
            'gender': 'F',
            'nationality': 'Canada',
            'country': 'Canada',
            'birthday': '2000-01-01',
            'email': 'test@user2.com',
            'company': self.testCompany2['companyName'],
            'position': 'Analyst',
            'phone': '0987654321',
            'is_entrepreneur': False,
            'entrepreneurship': '',
            'password': 'mypassword456'
        }
        self.testEmployee3 = {
            'first_name': 'Test',
            'last_name': 'Employee 3',
            'identification': '1234567890',
            'gender': 'M',
            'nationality': 'United States',
            'country': 'United States',
            'birthday': '2000-01-01',
            'email': 'test@user3.com',
            'company': self.testCompany1['companyName'],
            'position': 'Assistant',
            'phone': '1234567890',
            'is_entrepreneur': False,
            'entrepreneurship': '',
            'password': 'mypassword123'
        }
        self.testEmployee4 = {
            'first_name': 'Test',
            'last_name': 'Employee 4',
            'identification': '0987654321',
            'gender': 'F',
            'nationality': 'Canada',
            'country': 'Canada',
            'birthday': '2000-01-01',
            'email': 'test@user4.com',
            'company': self.testCompany2['companyName'],
            'position': 'Specialist',
            'phone': '0987654321',
            'is_entrepreneur': False,
            'entrepreneurship': '',
            'password': 'mypassword456'
        }
        
        # Enviar solicitudes POST para crear todas las empresas y empleados de prueba
        response = self.client.post(self.signup_business_url, data=self.testCompany1)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.signup_business_url, data=self.testCompany2)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.signup_user_url, data=self.testEmployee1)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.signup_user_url, data=self.testEmployee2)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.signup_user_url, data=self.testEmployee3)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.signup_user_url, data=self.testEmployee4)
        self.assertEqual(response.status_code, 302)
        
        self.section1 = Section.objects.create(name='Desempeño Contextual')
        self.section2 = Section.objects.create(name='Desempeño Contraproducente')
        self.section3 = Section.objects.create(name='Desempeño de Tarea')
        self.section4 = Section.objects.create(name='Estrategias de Comportamiento')
        self.section5 = Section.objects.create(name='Estrategias de Pensamiento Constructivo')
        self.section6 = Section.objects.create(name='Estrategias de Pensamiento de Recompensa')
        self.section7 = Section.objects.create(name='Autoliderazgo')
        self.section8 = Section.objects.create(name='Desempeño')
        self.section9 = Section.objects.create(name='Objetivos valores')
        self.section10 = Section.objects.create(name='Ayuda problema')
        self.section11 = Section.objects.create(name='Soporte trabajo')
        self.section12 = Section.objects.create(name='Trabajo interesante')
        self.section13 = Section.objects.create(name='Mis opiniones')
        self.section14 = Section.objects.create(name='Aumento salario')
        self.section15 = Section.objects.create(name='Apoyo Organizacional')
        
        # Crear las preguntas asociadas a las secciones
        questions_data = [
            {'description': 'Question 1', 'section_id': 1},
            {'description': 'Question 2', 'section_id': 1},
            {'description': 'Question 3', 'section_id': 1},
            {'description': 'Question 4', 'section_id': 1},
            {'description': 'Question 5', 'section_id': 1},
            {'description': 'Question 6', 'section_id': 1},
            {'description': 'Question 7', 'section_id': 1},
            {'description': 'Question 8', 'section_id': 1},
            {'description': 'Question 9', 'section_id': 2},
            {'description': 'Question 10', 'section_id': 2},
            {'description': 'Question 11', 'section_id': 2},
            {'description': 'Question 12', 'section_id': 2},
            {'description': 'Question 13', 'section_id': 2},
            {'description': 'Question 14', 'section_id': 3},
            {'description': 'Question 15', 'section_id': 3},
            {'description': 'Question 16', 'section_id': 3},
            {'description': 'Question 17', 'section_id': 3},
            {'description': 'Question 18', 'section_id': 4},
            {'description': 'Question 19', 'section_id': 4},
            {'description': 'Question 20', 'section_id': 4},
            {'description': 'Question 21', 'section_id': 4},
            {'description': 'Question 22', 'section_id': 4},
            {'description': 'Question 23', 'section_id': 4},
            {'description': 'Question 24', 'section_id': 4},
            {'description': 'Question 25', 'section_id': 4},
            {'description': 'Question 26', 'section_id': 4},
            {'description': 'Question 27', 'section_id': 5},
            {'description': 'Question 28', 'section_id': 5},
            {'description': 'Question 29', 'section_id': 5},
            {'description': 'Question 30', 'section_id': 5},
            {'description': 'Question 31', 'section_id': 5},
            {'description': 'Question 32', 'section_id': 5},
            {'description': 'Question 33', 'section_id': 5},
            {'description': 'Question 34', 'section_id': 6},
            {'description': 'Question 35', 'section_id': 6},
            {'description': 'Question 36', 'section_id': 6},
            {'description': 'Question 37', 'section_id': 9},
            {'description': 'Question 38', 'section_id': 10},
            {'description': 'Question 39', 'section_id': 11},
            {'description': 'Question 40', 'section_id': 12},
            {'description': 'Question 41', 'section_id': 13},
            {'description': 'Question 42', 'section_id': 14},
        ]

        for question_data in questions_data:
            Question.objects.create(description=question_data['description'], section_id=question_data['section_id'])
        
        
        
        # Hacer login con la compañia 1
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Test Form 1', '2022-01-01', '2022-01-31', ['1', '3', '4'], '["test@user1.com"]')
        self.assertEqual(response.status_code, 302)
        # Revisar si se creó el formulario
        form_exists = Form.objects.filter(title='Test Form 1').exists()
        self.assertTrue(form_exists)

        # La compañia 1 crea otro formulario con 3 secciones y 2 empleados
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Test Form 2', '2022-01-01', '2022-01-31', ['1', '2', '3'], '["test@user1.com", "test@user3.com"]')
        self.assertEqual(response.status_code, 302)
        # Revisar si se creó el formulario
        form_exists = Form.objects.filter(title='Test Form 2').exists()
        self.assertTrue(form_exists)
        
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Test Form 5', '2022-01-01', '2022-01-31', ['1', '2', '3', '4', '5', '6'], '["test@user1.com"]')
        self.assertEqual(response.status_code, 302)
        # Revisar si se creó el formulario
        form_exists = Form.objects.filter(title='Test Form 5').exists()
        self.assertTrue(form_exists)

        # Hacer login con la compañia 2
        response = self.create_form(self.testCompany2['email'], self.testCompany2['password'], 'Test Form 3', '2022-01-01', '2022-01-31', ['2', '5', '6'], '["test@user2.com"]')
        self.assertEqual(response.status_code, 302)
        # Revisar si se creó el formulario
        form_exists = Form.objects.filter(title='Test Form 3').exists()
        self.assertTrue(form_exists)

        # La compañia 2 crea otro formulario con 3 secciones y 2 empleados
        response = self.create_form(self.testCompany2['email'], self.testCompany2['password'], 'Test Form 4', '2022-01-01', '2022-01-31', ['2', '3', '5'], '["test@user2.com", "test@user4.com"]')
        self.assertEqual(response.status_code, 302)
        # Revisar si se creó el formulario
        form_exists = Form.objects.filter(title='Test Form 4').exists()
        self.assertTrue(form_exists)

    def create_form(self, email, password, title, start_date, end_date, selected_sections, employee_emails):
        response = self.client.post(self.signin_url, data={'email': email, 'password': password})
        self.assertEqual(response.status_code, 302)
        form_data = {
            'title': title,
            'start_date': start_date,
            'end_date': end_date,
            'selected_sections[]': selected_sections,
            'employee_emails': employee_emails
        }
        response = self.client.post(self.create_form_url, data=form_data)
        return response
    
    def test_result_form(self):
        # Iniciar sesión con el empleado 1
        response = self.client.post(self.signin_url, data={'email': self.testEmployee1['email'], 'password': self.testEmployee1['password']})
        self.assertEqual(response.status_code, 302)
        
        # Obtener el formulario creado por la compañía 1
        form = Form.objects.get(title='Test Form 2')
        #obtener id del empleado y del formulario
        employee_id = CustomUser.objects.get(email=self.testEmployee1['email']).id        
        # Obtener las preguntas asociadas al formulario
        questions = Question.objects.filter(section__in=form.sections.all())

        for question in questions:
            response = Response.objects.create(
                            employee=CustomUser.objects.get(email=self.testEmployee1['email']),
                            form=form,
                            section=question.section,
                            question=question,
                            answer=random.randint(1, 5)  # Choose a random answer between 1 and 5
                        )

        # Verificar si se crearon las respuestas en la base de datos
        responses_exist = Response.objects.filter(form=form, employee=employee_id).exists()
        self.assertTrue(responses_exist)

        # Llamo funcion para el calculo de resultados
        response = self.client.post(self.resul_user_url)
        self.assertEqual(response.status_code, 200) #Verificar que la respuesta sea exitosa

        
        # Verificar si se crearon los resultados en la base de datos
        # results_exist = ResultadosUsuario.objects.filter(id_empleado=employee_id)
        # print(results_exist.values())
    
    def test_create_form(self):
        # Iniciar sesión con la compañía 1
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Test Form 1', '2022-01-01', '2022-01-31', ['1', '3', '4'], '["test@user1.com"]')
        self.assertEqual(response.status_code, 302)
        # Revisar si se creó el formulario
        form_exists = Form.objects.filter(title='Test Form 1').exists()
        self.assertTrue(form_exists)
        
        # Crear otro formulario con 2 empleados
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Test Form 2', '2022-01-01', '2022-01-31', ['1', '2', '3'], '["test@user1.com", "test@user3.com"]')
        self.assertEqual(response.status_code, 302)
        form_exists = Form.objects.filter(title='Test Form 2').exists()
        self.assertTrue(form_exists)
    
    def test_result_Empre(self):
        # Iniciar sesión con el empleado 1
        response = self.client.post(self.signin_url, data={'email': self.testEmployee1['email'], 'password': self.testEmployee1['password']})
        self.assertEqual(response.status_code, 302)
        
        # Obtener el formulario creado por la compañía 2
        form = Form.objects.get(title='Test Form 2')
        employee_id = CustomUser.objects.get(email=self.testEmployee1['email']).id
        questions = Question.objects.filter(section__in=form.sections.all())

        for question in questions:
            response = Response.objects.create(
                            employee=CustomUser.objects.get(email=self.testEmployee1['email']),
                            form=form,
                            section=question.section,
                            question=question,
                            answer=random.randint(1, 5)  # Choose a random answer between 1 and 5
                        )

        # Verificar si se crearon las respuestas en la base de datos
        responses_exist = Response.objects.filter(form=form, employee=employee_id).exists()
        self.assertTrue(responses_exist)

        # Llamo funcion para el calculo de resultados
        response = self.client.post(self.resul_user_url)
        self.assertEqual(response.status_code, 200) #Verificar que la respuesta sea exitosa
        # Verificar si se crearon los resultados en la base de datos
        results_exist = ResultadosUsuario.objects.filter(id_empleado=employee_id)



        # Iniciar sesión con el empleado 3
        response = self.client.post(self.signin_url, data={'email': self.testEmployee3['email'], 'password': self.testEmployee3['password']})
        self.assertEqual(response.status_code, 302)
        
        # Obtener el formulario creado por la compañía 2
        form = Form.objects.get(title='Test Form 2')
        employee_id = CustomUser.objects.get(email=self.testEmployee3['email']).id
        questions = Question.objects.filter(section__in=form.sections.all())

        for question in questions:
            response = Response.objects.create(
                            employee=CustomUser.objects.get(email=self.testEmployee3['email']),
                            form=form,
                            section=question.section,
                            question=question,
                            answer=random.randint(1, 5)  # Choose a random answer between 1 and 5
                        )

        # Verificar si se crearon las respuestas en la base de datos
        responses_exist = Response.objects.filter(form=form, employee=employee_id).exists()
        self.assertTrue(responses_exist)

        # Llamo funcion para el calculo de resultados
        response = self.client.post(self.resul_user_url)
        self.assertEqual(response.status_code, 200) #Verificar que la respuesta sea exitosa
        
        # Verificar si se crearon los resultados en la base de datos
        results_exist = ResultadosUsuario.objects.filter(id_empleado=employee_id)
        # print(results_exist.values())

        # Iniciar sesión con la empresa
        response = self.client.post(self.signin_url, data={'email': self.testCompany1['email'], 'password': self.testCompany1['password']})
        self.assertEqual(response.status_code, 302)
        empresa_id = Company.objects.get(email=self.testCompany1['email']).id

        # Llamo funcion para el calculo de resultados de la empresa
        response = self.client.post(self.resul_Empre_url)
        
        results_exist = ResultadosEmpresa.objects.filter(id_empresa=empresa_id)