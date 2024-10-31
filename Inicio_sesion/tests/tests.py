from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate

from Inicio_sesion.models import Company

# Create your tests here.
class SignUpBusinessTest(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas
        self.signup_business_url = reverse('Inicio_sesion:signup_business')
        self.valid_data = {
            'companyName': 'Mi Empresa',
            'dateFoundation': '2022-01-01',
            'email': 'empresa@example.com',
            'NIT': '1234567890',
            'phone': '1234567890',
            'country': 'United States',
            'password': 'mypassword123'
        }
        self.invalid_data = {
            'companyName': 'Otra Empresa',
            'dateFoundation': '2023-01-01',
            'email': 'empresa@example.com',  # Correo ya registrado
            'NIT': '1234567890',
            'phone': '0987654321',
            'country': 'Canada',
            'password': 'mypassword456'
        }
        self.another_invalid_data = {
            'companyName': 'Mi Empresa',  # Nombre ya registrado
            'dateFoundation': '2024-01-01',
            'email': 'otraempresa@example.com',
            'NIT': '0987654321',
            'phone': '1122334455',
            'country': 'Mexico',
            'password': 'anotherpassword789'
        }
    
    def test_create_company_valid(self):
        response = self.client.post(self.signup_business_url, data=self.valid_data) # Enviar la solicitud POST para crear una empresa
        self.assertEqual(response.status_code, 302) # Verificar que la respuesta sea exitosa, se espera un código 302 por redirección después del registro
        # Verificar que la empresa se haya guardado en la base de datos con el nombre correcto
        company_exists = Company.objects.filter(companyName=self.valid_data['companyName']).exists()
        self.assertTrue(company_exists)

        # Verificacion de los datos
        company = Company.objects.get(companyName=self.valid_data['companyName'])
        foundation_date_str = company.foundationDate.strftime('%Y-%m-%d')# Convertir el objeto datetime.date a cadena
        self.assertEqual(foundation_date_str, self.valid_data['dateFoundation'])
        self.assertEqual(company.email, self.valid_data['email'])
        self.assertEqual(company.phone, self.valid_data['phone'])
        self.assertEqual(company.country, self.valid_data['country'])
    

    def test_create_company_invalid(self):
        # Crear la empresa inicialmente con datos válidos
        self.client.post(self.signup_business_url, data=self.valid_data)
        
        # Intentar crear otra empresa con un correo ya registrado (debe fallar)
        response = self.client.post(self.signup_business_url, data=self.invalid_data)
        self.assertEqual(response.status_code, 200)  # Verificar que la respuesta sea exitosa
        # Verificar que no se haya creado una nueva empresa con el mismo correo
        company_count = Company.objects.filter(email='empresa@example.com').count()
        self.assertEqual(company_count, 1)

    def test_create_company_invalid_name(self):
        # Crear la empresa inicialmente con datos válidos
        self.client.post(self.signup_business_url, data=self.valid_data)
        
        # Intentar crear otra empresa con un correo ya registrado (debe fallar)
        response = self.client.post(self.signup_business_url, data=self.invalid_data)
        self.assertEqual(response.status_code, 200)  # Verificar que la respuesta sea exitosa
        # Verificar que no se haya creado una nueva empresa con el mismo correo
        company_count = Company.objects.filter(companyName='Mi Empresa').count()
        self.assertEqual(company_count, 1)
        
class LoginTest(TestCase):
    def setUp(self):
        self.signup_business_url = reverse('Inicio_sesion:signup_business')
        # Configuración inicial para las pruebas
        self.login_url = reverse('Inicio_sesion:signin')
        self.user_credentials = {
            'email': 'empresa@example.com',
            'password': 'mypassword123'
        }
        self.user_credentials_incorrect = {
            'email': 'empresa@example.com',
            'password': 'mypassword1234'
        }
        # Crear un usuario para la prueba
        self.user_credentials_create = {
            'companyName': 'Mi Empresa',
            'dateFoundation': '2022-01-01',
            'email': 'empresa@example.com',
            'NIT': '1234567890',
            'phone': '1234567890',
            'country': 'United States',
            'password': 'mypassword123'
        }

    def test_login_success(self):
        response = self.client.post(self.signup_business_url, data=self.user_credentials_create) # Enviar la solicitud POST para crear una empresa
        self.assertEqual(response.status_code, 302)
        responseLogin = self.client.post(self.login_url, data=self.user_credentials)
        self.assertEqual(responseLogin.status_code, 302)
        user = authenticate(username=self.user_credentials['email'], password=self.user_credentials['password'])
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)

    def test_login_unsuccess(self):
        response = self.client.post(self.signup_business_url, data=self.user_credentials_create) # Enviar la solicitud POST para crear una empresa
        self.assertEqual(response.status_code, 302)
        responseLogin = self.client.post(self.login_url, data=self.user_credentials_incorrect)
        self.assertEqual(responseLogin.status_code, 200)
        user = authenticate(username=self.user_credentials_incorrect['email'], password=self.user_credentials_incorrect['password'])
        self.assertIsNone(user)

#Comando para ejecutar las pruebas de inicio sesion y registro de empresas
#python manage.py test Inicio_sesion.tests.tests