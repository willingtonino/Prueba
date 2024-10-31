import json
from pyexpat.errors import messages
from sqlite3 import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from Inicio_sesion.models import CustomUser, Company
from Formulario.models import Form, Section, FormSection
from django.contrib.auth.models import User
from .models import Form, Question, Response
from Resultados.views import resultadosUsuarios




def index(request):
    """
    Index view
    """
    return HttpResponse("This is an index page")


def userView(request):
    """
    View for userView.html
    """
    # Obtén el correo electrónico de la sesión
    email = request.session.get("user_email")
    if email:
        # Obten informacion del usuario
        user_info = CustomUser.objects.get(email=email)        
        # Convertir la información del usuario en un diccionario para poder pasarla a la plantilla
        
        # Unanswered forms
        # Obtener todas las respuestas asociadas al usuario
        responses = Response.objects.filter(employee=user_info)
        
        # Obtener el listado de formularios a los que el usuario tiene acceso y que no ha respondido, es decir, que no tienen una respuesta asociada
        forms = Form.objects.filter(authorized_employees=user_info)
        completed_forms = []  # Create an empty list for completed forms
        #print("All Forms:", forms)
        for form in forms:
            if form.id in responses.values_list("form_id", flat=True):
                forms = forms.exclude(id=form.id)
                completed_forms.append(form)  # Add the excluded form to the completed_forms list
        #print("Incomplete Forms:", forms)
        #print("Completed Forms:", completed_forms)
            
            
        
        # Convertir el queryset de formularios en una lista de diccionarios con título y fecha de finalización para poder pasarlo a la plantilla
        forms = [{"title": form.title, "end_date": form.end_date} for form in forms]
        #print("Forms:", forms)
        # Obtener todos los registros de respuestas asociados al usuario
        responses = Response.objects.filter(employee=user_info)
        # Agregar a la lista de pending_forms todo formulario que no tenga una respuesta asociada
        pending_forms = Form.objects.filter(authorized_employees=user_info).exclude(id__in=responses.values_list("form_id", flat=True))
        # print("Pending Forms:", pending_forms)
        # Agregar a la lista de completed_forms todo formulario que tenga una respuesta asociada
        completed_forms = Form.objects.filter(authorized_employees=user_info).filter(id__in=responses.values_list("form_id", flat=True))
        # print("Completed Forms:", completed_forms)

        #print("Responses:", responses)

        user_info_dict = {
            "first_name": user_info.first_name,
            "last_name": user_info.last_name,
            "identification": user_info.identification,
            "gender": user_info.gender,
            "nationality": user_info.nationality,
            "country": user_info.country,
            "birthday": user_info.birthday,
            "email": user_info.email,
            "company": user_info.company.companyName,
            "position": user_info.position,
            "phone": user_info.phone,
            "forms": forms,
            "responses": responses,
            "pending_forms": pending_forms,
            "completed_forms": completed_forms
        }
        if user_info:
            # Pasa la información del usuario a la plantilla para renderizarla
            return render(request, "Formulario/ViewUser.html", {"user_info": user_info_dict})
        else:
            return HttpResponse("Error retrieving user information")
    else:
        return HttpResponse("Email not provided in session")


def companyView(request):
    """
    View for companyView.html
    """
    # Obtén el correo electrónico de la sesión
    email = request.session.get("user_email")
    # #print("User Email in Session:", email)
    if email:
        # Obtén información de la compañía
        company = Company.objects.get(email=email)
        # Obtén todos los empleados de la compañía
        employees = CustomUser.objects.filter(company_id=company)
        # Turn the employees queryset into a list of dictionaries with name and position so it can be passed to the template
        employees = [
            {"name": employee.first_name + " " + employee.last_name, "position": employee.position}
            for employee in employees
        ]
        #print("Employees:", employees)
        # Obten todos los formularios de la compañía
        forms = Form.objects.filter(company=company)
        # Turn the forms queryset into a list of dictionaries with title and end date so it can be passed to the template
        forms = [{"title": form.title, "end_date": form.end_date} for form in forms]
        
        context = {
            "company_info": company,
            "employees": employees,
            "forms": forms,
        }
        
        if company:
            # Pasa la información de la compañía a la plantilla para renderizarla
            #print("Context:", {"company_info": company, "employees": employees})
            return render(
                request, "Formulario/ViewCompany.html", context
            )
        else:
            return HttpResponse("Error retrieving company information")
    else:
        authenticatable_users = User.objects.filter(password__isnull=False).exclude(
            password=""
        )
        #print("Authenticatable Users:")
        for user in authenticatable_users:
            print(user.username)
        return HttpResponse("Email not provided in session")


def editUserProfileView(request):
    email = request.session.get("user_email")
    print(f"Email: {email}")

    if email:
        user_info = CustomUser.objects.get(email=email)
        print(f"User Info: {user_info}")

        if request.method == 'POST':
            update_user_profile(user_info, request.POST)
            return redirect('Formulario:userView')  # Redirige a la vista del usuario después de actualizar

        formatted_date = user_info.birthday.strftime("%Y-%m-%d")        

        user_info_dict = {
            "first_name": user_info.first_name,
            "last_name": user_info.last_name,
            "identification": user_info.identification,
            "gender": user_info.gender,
            "nationality": user_info.nationality,
            "country": user_info.country,
            "birthday": formatted_date,
            "email": user_info.email,
            "company": user_info.company.companyName,
            "position": user_info.position,
            "phone": user_info.phone,
            "isEntrepreneur": user_info.is_entrepreneur,
            "entrepreneurship": user_info.entrepreneurship,
        }
        return render(request, "Formulario/editUserInfo.html", {"user_info": user_info_dict})
    else:
        return HttpResponse("Email not provided in session")

def update_user_profile(user_info, data):
    user_info.first_name = data.get("first_name")
    user_info.last_name = data.get("last_name")
    user_info.identification = data.get("identification")
    user_info.gender = data.get("gender")
    user_info.nationality = data.get("nationality")
    user_info.country = data.get("country")
    user_info.birthday = data.get("birthday")
    user_info.position = data.get("position")
    user_info.phone = data.get("phone")
    user_info.is_entrepreneur = data.get("isEntrepreneur") == "True"
    user_info.entrepreneurship = data.get("entrepreneurship") if user_info.is_entrepreneur else ""

    user_info.save()
    

def editCompanyProfileView(request):
    email = request.session.get("user_email")
    print(f"Email: {email}")

    if email:
        try:
            company_info = Company.objects.get(email=email)
            print(f"Company Info: {company_info}")

            if request.method == 'POST':
                update_company_profile(company_info, request.POST)
                return redirect('Formulario:companyView')  # Redirige a la vista de la compañía después de actualizar

            formatted_date = company_info.foundationDate.strftime("%Y-%m-%d")

            company_info_dict = {
                "companyName": company_info.companyName,
                "dateFoundation": formatted_date,
                "email": company_info.email,
                "NIT": company_info.NIT,
                "phone": company_info.phone,                
                "country": company_info.country,
            }
            return render(request, "Formulario/editCompanyInfo.html", {"company_info": company_info_dict})
        except Company.DoesNotExist:
            return HttpResponse("Error retrieving company information")
    else:
        return HttpResponse("Email not provided in session")

def update_company_profile(company_info, data):
    company_info.companyName = data.get("companyName")
    company_info.foundationDate = data.get("dateFoundation")
    company_info.phone = data.get("phone")
    company_info.NIT = data.get("NIT")
    company_info.country = data.get("country")

    company_info.save()

    # If there's additional business logic needed when company info is updated, handle it here.
    # For example, if you need to log this update or trigger other updates.
    
    
def uploadProfilePicture(request):
    return HttpResponse("You are trying to upload a picture")


def createFormView(request):
    if request.method == "POST":
        # Handle POST request to render the create form view
        user_email = request.session.get("user_email")
        company_info = Company.objects.get(email=user_email)
        return render(
            request, "Formulario/tempCreateForm.html", {"company_info": company_info}
        )
    else:

        # Redirect to a error page or reload the current page
        return HttpResponse(
            "Error entering form view"
        )  # Assuming 'dashboard' is the URL name for the dashboard view

def createForm(request):
    if request.method == "POST":
        # Obtener los datos del formulario enviado por el usuario
        #print("ENTRANDO A CREAR FORMULARIO")
        title = request.POST.get("title")
        #print("Title:", title)
        start_date = request.POST.get("start_date")
        #print("Start Date:", start_date)
        end_date = request.POST.get("end_date")
        #print("End Date:", end_date)
        selected_sections = Section.objects.filter(id__in=[1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14])
        # selected_sections = request.POST.getlist(
        #     "selected_sections[]"
        # )  # Obtener las secciones seleccionadas

        # crear un selected_sections con todas las secciones
        all_sections = Section.objects.all()
        
        
        print("Selected Sections:", selected_sections)
        django_user = request.user  # Assuming request.user is the Django user
        # Obtener la compañía autenticada actualmente
        company = get_object_or_404(Company, email=django_user.email)

        # Convertir el JSON de empleados autorizados a una lista de correos electrónicos
        employee_emails_json = request.POST.get("employee_emails")
        # Imprimir la lista completa de correos electrónicos para verificar
        employee_emails = (
            json.loads(employee_emails_json) if employee_emails_json else []
        )

        # Validar que la fecha de finalización no sea anterior a la fecha de inicio
        if end_date < start_date:
            response = HttpResponse("End date cannot be before start date")
            response['X-Error-Type'] = 'date_mismatch'
            return response

        # Validar que la compañía solo pueda asignar empleados registrados bajo ella
        unregistered_employees = set(employee_emails) - set(company.customuser_set.values_list('email', flat=True))
        if unregistered_employees:
            response = HttpResponse(f"The following employees are not registered under the company: {', '.join(unregistered_employees)}")
            response['X-Error-Type'] = 'unregistered_employees'
            return response

        # Validar que se hayan seleccionado al menos una sección para el formulario
        if selected_sections == []:
            response = HttpResponse("Cannot create a form without sections")
            response['X-Error-Type'] = 'no_sections_selected'
            return response

        # Validar que se haya proporcionado un título para el formulario
        if title == "":
            response = HttpResponse("Cannot create a form without a title")
            response['X-Error-Type'] = 'no_title'
            return response
        
        # Crear el formulario con los datos proporcionados
        form = Form.objects.create(
            title=title,
            company=company,
            start_date=start_date,
            end_date=end_date,
        )

        # Agregar secciones seleccionadas al formulario a partir del identificador de la sección
        sections = Section.objects.filter(id__in=selected_sections)
        form.sections.set(sections)
        #print(f"Secciones seleccionadas y agregadas: {sections}")

        # Agregar empleados autorizados al formulario
        authorized_employees = CustomUser.objects.filter(email__in=employee_emails)
        form.authorized_employees.set(authorized_employees)
        #print(f'Empleados autorizados: {authorized_employees}')

        # Crear relaciones entre el formulario y las secciones seleccionadas
        for section in sections:
            if not FormSection.objects.filter(form=form, section=section).exists():
                FormSection.objects.create(form=form, section=section)

        # Guardar el formulario y redirigir o renderizar según sea necesario
        form.save()
        #print("Formulario creado:", form)
        # Mostrar todos los atributos del formulario creado
        #print(f"Formulario creado: {form.title}, {form.company}, {form.start_date}, {form.end_date}, {form.sections.all()}, {form.authorized_employees.all()}")

        # Renderizar la plantilla HTML con los detalles del formulario creado
        return redirect('Formulario:companyView')

    # Logic to render the create form page if it is not a POST request or if the form is not valid
    return render(request, "Formulario/tempCreateForm.html")


def userFormView(request):
    form_title = request.GET.get('form_title')  # Retrieve form_title from query parameters
    form = Form.objects.get(title=form_title)
    #print("Form:", form)
    # Turn form into a dictionary to pass it to the template
    form = {
        "title": form.title,
        "company": form.company.companyName,
        "start_date": form.start_date,
        "end_date": form.end_date,
        "sections": form.sections.all(),
    }
    #print("Form:", form)    
    options = [1, 2, 3, 4, 5]  # List of options
    
    context = {
        'form': form,
        'range_1_to_5': list(range(1, 6)),

    }
    return render(request, 'Formulario/tempUserFormView.html', {"context": context})

def submitForm(request):
    if request.method == 'POST':
        #print("Se recibio un POST")
        for key, value in request.POST.items():
            if key.startswith('response_'):
                _, form_id, section_id, question_id = key.split('_')
                #print(f"Form ID: {form_id}, Section ID: {section_id}, Question ID: {question_id}, Answer: {value}")
                # Uncomment the following lines to save the responses
                section = Section.objects.get(id=section_id)
                question = Question.objects.get(id=question_id)
                form = Form.objects.get(title=form_id)
                employee = CustomUser.objects.get(email=request.user.email)
                Response.objects.create(
                    employee=employee,
                    form=form,
                    section=section,
                    question=question,
                    answer=value
                )
        resultadosUsuarios(request)
        return redirect('Formulario:userView')