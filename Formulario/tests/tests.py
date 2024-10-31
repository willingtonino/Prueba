from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import CustomUser, Company, Form, Section, FormSection, Question, Response
from django.contrib.auth.models import User
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
            {'description': 'Question 32', 'section_id': 6},
            {'description': 'Question 33', 'section_id': 6},
            {'description': 'Question 34', 'section_id': 6},
        ]

        for question_data in questions_data:
            Question.objects.create(description=question_data['description'], section_id=question_data['section_id'])
    
        
        # Hacer login con la compañia 1
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Test Form', '2022-01-01', '2022-01-31', ['1', '3', '4'], '["test@user1.com"]')
        self.assertEqual(response.status_code, 302)
        # Revisar si se creó el formulario
        form_exists = Form.objects.filter(title='Test Form').exists()
        self.assertTrue(form_exists)

        # La compañia 1 crea otro formulario con 3 secciones y 2 empleados
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Test Form 2', '2022-01-01', '2022-01-31', ['1', '2', '3'], '["test@user1.com", "test@user3.com"]')
        self.assertEqual(response.status_code, 302)
        # Revisar si se creó el formulario
        form_exists = Form.objects.filter(title='Test Form 2').exists()
        self.assertTrue(form_exists)
        
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Test Form 5', '2022-01-01', '2022-01-31', ['1', '2', '3'], '["test@user1.com"]')
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

        
        # Verificar que las empresas y empleados se hayan guardado en la base de datos
        # company1_exists = Company.objects.filter(companyName=self.testCompany1['companyName']).exists()
        # company2_exists = Company.objects.filter(companyName=self.testCompany2['companyName']).exists()
        # employee1_exists = CustomUser.objects.filter(email=self.testEmployee1['email']).exists()
        # employee2_exists = CustomUser.objects.filter(email=self.testEmployee2['email']).exists()
        # employee3_exists = CustomUser.objects.filter(email=self.testEmployee3['email']).exists()
        # employee4_exists = CustomUser.objects.filter(email=self.testEmployee4['email']).exists()
        # self.assertTrue(company1_exists)
        # self.assertTrue(company2_exists)
        # self.assertTrue(employee1_exists)
        # self.assertTrue(employee2_exists)
        # self.assertTrue(employee3_exists)
        # self.assertTrue(employee4_exists)
        
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
    
    def test_create_form(self):
        # Iniciar sesión con la compañía 1
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Title1', '2022-01-01', '2022-01-31', ['1', '3', '4'], '["test@user1.com"]')
        self.assertEqual(response.status_code, 302)
        # Revisar si se creó el formulario
        form_exists = Form.objects.filter(title='Title1').exists()
        self.assertTrue(form_exists)
        
        # Crear otro formulario con 2 empleados
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Title2', '2022-01-01', '2022-01-31', ['1', '2', '3'], '["test@user1.com", "test@user3.com"]')
        self.assertEqual(response.status_code, 302)
        form_exists = Form.objects.filter(title='Title2').exists()
        self.assertTrue(form_exists)
        
        
    def test_form_end_date_before_start_date(self):
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Test Form', '2022-02-01', '2022-01-31', ['1', '2', '3'], '["test@user1.com"]')
        self.assertIn('X-Error-Type', response)
        self.assertEqual(response['X-Error-Type'], 'date_mismatch')

    def test_form_with_unregistered_employee(self):
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Test Form', '2022-01-01', '2022-01-31', ['1', '2', '3'], '["unregistered@user.com"]')
        self.assertIn('X-Error-Type', response)
        self.assertEqual(response['X-Error-Type'], 'unregistered_employees')

    def test_form_without_sections(self):
        response = self.create_form(self.testCompany1['email'], self.testCompany1['password'], 'Test Form', '2022-01-01', '2022-01-31', [], '["test@user1.com", "test@user3.com"]')
        self.assertIn('X-Error-Type', response)
        self.assertEqual(response['X-Error-Type'], 'no_sections_selected')

    def test_form_without_title(self):
        response = self.create_form(self.testCompany2['email'], self.testCompany2['password'], '', '2022-01-01', '2022-01-31', ['1', '2', '3'], '["test@user2.com"]')
        self.assertIn('X-Error-Type', response)
        self.assertEqual(response['X-Error-Type'], 'no_title')
        
        
    def test_view_employee_info(self):     
        # Iniciar sesión con el empleado 1
        response = self.client.post(self.signin_url, data={'email': self.testEmployee1['email'], 'password': self.testEmployee1['password']})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.user_view_url)
        self.assertEqual(response.status_code, 200)
        # Verificar que el empleado 1 pueda ver los formularios a los que está autorizado
        user_info_dict = response.context['user_info']
        self.assertEqual(user_info_dict['first_name'], self.testEmployee1['first_name'])
        self.assertEqual(user_info_dict['last_name'], self.testEmployee1['last_name'])
        self.assertEqual(user_info_dict['identification'], self.testEmployee1['identification'])
        self.assertEqual(user_info_dict['gender'], self.testEmployee1['gender'])
        self.assertEqual(user_info_dict['nationality'], self.testEmployee1['nationality'])
        self.assertEqual(user_info_dict['country'], self.testEmployee1['country'])
        self.assertEqual(str(user_info_dict['birthday']), self.testEmployee1['birthday'])
        self.assertEqual(user_info_dict['email'], self.testEmployee1['email'])
        self.assertEqual(user_info_dict['company'], self.testEmployee1['company'])
        self.assertEqual(user_info_dict['position'], self.testEmployee1['position'])
        self.assertEqual(user_info_dict['phone'], self.testEmployee1['phone'])
        
    def test_view_employee_assigned_forms(self):
        # Iniciar sesión con el empleado 1
        response = self.client.post(self.signin_url, data={'email': self.testEmployee1['email'], 'password': self.testEmployee1['password']})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.user_view_url)
        self.assertEqual(response.status_code, 200)
        # Verificar que el empleado 1 pueda ver los formularios a los que está autorizado
        forms = Form.objects.filter(authorized_employees__email=self.testEmployee1['email'])
        forms_info = [{'title': form.title, 'end_date': form.end_date} for form in forms]
        user_info_dict = response.context['user_info']
        self.assertEqual(user_info_dict['forms'], forms_info)
        
    def test_view_employee_answered_unanswered_forms(self):
        # Iniciar sesión con el empleado 1
        response = self.client.post(self.signin_url, data={'email': self.testEmployee1['email'], 'password': self.testEmployee1['password']})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.user_view_url)
        self.assertEqual(response.status_code, 200)
        forms = Form.objects.filter(authorized_employees__email=self.testEmployee1['email'])
        for form in forms:
            if form.title == 'Test Form 5':
                sections = form.sections.all()
                for section in sections:
                    questions = section.questions.all()
                    for question in questions:
                        response = Response.objects.create(
                            employee=CustomUser.objects.get(email=self.testEmployee1['email']),
                            form=form,
                            section=section,
                            question=question,
                            answer=random.randint(1, 5)  # Choose a random answer between 1 and 5
                        )
                        response.save()
                        

        # Verificar que todas las respuestas asociadas al empleado 1 y al formulario 5 se hayan guardado
        # Contar el numero de preguntas que esten asociadas con las secciones del formulario 5
        form = Form.objects.get(title='Test Form 5')
        sections = form.sections.all()
        responses = Response.objects.filter(employee__email=self.testEmployee1['email'], form__title='Test Form 5')
        # Print all attributes of sections
        question_count = 0
        for response in responses:
            # Count the number of questions associated with the section id
            if response.section.id in [section.id for section in sections]:
                question_count += 1
        
        # expected_answers = sum([section.questions.count() for section in sections])
        responses = Response.objects.filter(employee__email=self.testEmployee1['email'], form__title='Test Form 5')
        self.assertEqual(len(responses), question_count)
       

        response = self.client.get(self.user_view_url)
        self.assertEqual(response.status_code, 200)
        user_info_dict = response.context['user_info']
        forms = Form.objects.filter(authorized_employees__email=self.testEmployee1['email'])

        
        # Obtener el listado pending_forms, que es todo formulario que no tenga respuesta
        pending_forms = []
        completed_forms = []
        for form in forms:
            responses = Response.objects.filter(employee__email=self.testEmployee1['email'], form=form)
            if not responses:
                pending_forms.append(form)
            else:
                completed_forms.append(form)
                

        self.assertEqual(list(user_info_dict["pending_forms"]), pending_forms)
        self.assertEqual(list(user_info_dict["completed_forms"]), completed_forms)
        



        
    