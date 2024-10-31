import os
import django
from datetime import date
import sys

# Configura el entorno Django
sys.path.append('C:/Users/josen/Desktop/Uni/SisInfo/ADAP/ADAP/ADAP')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ADAP.settings')
django.setup()

from Inicio_sesion.models import Company, CustomUser
from Inicio_sesion.views import signup, signup_business

def create_test_data():
    # Datos de prueba para las compañías
    company_data_1 = {
        'companyName': "Company Test 1",
        'dateFoundation': date(2000, 1, 1),
        'email': "company1@test.com",
        'NIT': "1234567890",
        'phone': "1234567890",
        'country': "Testland",
        'password': "company1password"
    }
    company1 = signup_business(company_data=company_data_1)

    company_data_2 = {
        'companyName': "Company Test 2",
        'dateFoundation': date(2005, 5, 5),
        'email': "company2@test.com",
        'NIT': "0987654321",
        'phone': "0987654321",
        'country': "Testlandia",
        'password': "company2password"
    }
    company2 = signup_business(company_data=company_data_2)

    # Datos de prueba para los empleados
    user_data_1 = {
        'first_name': "John",
        'last_name': "Doe",
        'identification': "ID12345",
        'gender': "M",
        'nationality': "Testland",
        'phone': "1234567890",
        'country': "Testland",
        'birthday': date(1990, 1, 1),
        'email': "john.doe@company1.com",
        'company_name': "Company Test 1",
        'position': "Developer",
        'is_entrepreneur': False,
        'entrepreneurship': "",
        'password': "johndoepassword"
    }
    signup(user_data=user_data_1)

    user_data_2 = {
        'first_name': "Jane",
        'last_name': "Smith",
        'identification': "ID54321",
        'gender': "F",
        'nationality': "Testland",
        'phone': "0987654321",
        'country': "Testland",
        'birthday': date(1992, 2, 2),
        'email': "jane.smith@company1.com",
        'company_name': "Company Test 1",
        'position': "Manager",
        'is_entrepreneur': False,
        'entrepreneurship': "",
        'password': "janesmithpassword"
    }
    signup(user_data=user_data_2)

    user_data_3 = {
        'first_name': "Alice",
        'last_name': "Johnson",
        'identification': "ID67890",
        'gender': "F",
        'nationality': "Testlandia",
        'phone': "1231231234",
        'country': "Testlandia",
        'birthday': date(1995, 3, 3),
        'email': "alice.johnson@company2.com",
        'company_name': "Company Test 2",
        'position': "Analyst",
        'is_entrepreneur': False,
        'entrepreneurship': "",
        'password': "alicejohnsonpassword"
    }
    signup(user_data=user_data_3)

    user_data_4 = {
        'first_name': "Bob",
        'last_name': "Brown",
        'identification': "ID09876",
        'gender': "M",
        'nationality': "Testlandia",
        'phone': "4321432143",
        'country': "Testlandia",
        'birthday': date(1997, 4, 4),
        'email': "bob.brown@company2.com",
        'company_name': "Company Test 2",
        'position': "Tester",
        'is_entrepreneur': False,
        'entrepreneurship': "",
        'password': "bobbrownpassword"
    }
    signup(user_data=user_data_4)

    print("Datos de prueba creados exitosamente.")

if __name__ == "__main__":
    create_test_data()
