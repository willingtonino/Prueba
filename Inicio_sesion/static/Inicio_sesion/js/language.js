console.log('Hello from main.js!')

const en = {
    "form": {
        "title": "Log In",
        "submit-btn": "Log In"
    },
    "placeholder": {
        "email": "Email",
        "passwords": "Password"
    },
    "links": {
        "forgot-password": "Forgot Password?",
        "create-account": "Create an account"
        
    },
    "FSign":{
        "Names": "Names",
        "Surnames": "Surnames",
        "ID": "ID",
        "Gender": "Gender",
        "GSelect":"Select your gender",
        "Gm":"Male",
        "Gf":"Female",
        "Go":"Other",
        "Nationality": "Nationality",
        "NSelect": "Select your nationality",
        "Phone": "Phone",
        "Password": "Password",
        "Country of Residence": "Country of Residence",
        "RSelect": "Select your country of residence",
        "Date of Birth": "Date of Birth",
        "E-mail": "E-mail",
        "Company": "Company",
        "Position in the company": "Position in the company",
        "Position":"Select your position",
        "Areyou": "Are you an entrepreneur?",
        "Entrepreneurship": "Entrepreneurship",
        "Conditions": "I have read and accept the Terms and Conditions",
        "Register": "Register",
        "Registro1": "Are you a company? You can register as a company:",
        "registroc":"Here",
        "Registro2": "Are you not a company? You can register as a user:",
        "Date of fundation":"Date of fundation",
        "CName":"Company Name"

    },
    "Verificacion":{
        "AUT": "Two-Step Authentication",
        "security-code-label": "Enter security code sent to your email:",
        "password-label": "Password:",
        "terms-label": "I accept the terms and conditions",
        "submit-btnAUT": "Sign In"

    }
  }
  

const es =  {
    "form": {
        "title": "Iniciar sesión",
        "submit-btn": "Iniciar sesión"
    },
    "placeholder": {
        "email": "Correo electrónico",
        "password": "Contraseña"
    },
    "links": {
        "forgot-password": "¿Olvidaste tu contraseña?",
        "create-account": "Crear una cuenta"
    },
    "FSign":{
        "Names": "Nombres",
        "Surnames": "Apellidos",
        "ID": "Documento de identidad",
        "Gender": "Género",
        "GSelect":"Selecciona tu genero",
        "Gm":"Masculino",
        "Gf":"Femenino",
        "Go":"Otro",
        "Nationality": "Nacionalidad",
        "NSelect":"Seleccione su nacionalidad",
        "Phone": "Teléfono",
        "Password": "Contraseña",
        "Country of Residence": "País de residencia",
        "RSelect": "Seleccione su pais de residencia",
        "Date of Birth": "Fecha de nacimiento",
        "E-mail": "Correo electrónico",
        "Company": "Empresa",
        "Position in the company": "Cargo en la empresa",
        "Position":"Seleccione su cargo",
        "Areyou": "¿Eres emprendedor?",
        "Entrepreneurship": "Emprendimiento",
        "Conditions": "He leído y acepto los Términos y Condiciones",
        "Register": "Registrarse",
        "Registro1": "¿Eres una compañia? Puedes registrarte como compañia:",
        "registroc":"Aqui",
        "Registro2": "¿No eres una compañia? Puedes registrarte como usuario:",
        "Date of fundation":"Fecha de fundacion",
        "CName":"Nombre de la empresa"
    },
    "Verificacion":{
        "AUT": "Autenticación de Dos Pasos",
        "security-code-label": "Ingrese el código de seguridad enviado a su correo electrónico:",
        "password-label": "Contraseña:",
        "terms-label": "Acepto los términos y condiciones",
        "submit-btn": "Iniciar Sesión"

    }
}

const flagsElement =  document.getElementById('flags');
const textsToChange = document.querySelectorAll("[data-section]");

const changeLanguage = (lang) => {
    const texts = lang === 'es' ? es : en;
    for (textToChange of textsToChange) {
        const section = textToChange.dataset.section;
        const value = textToChange.dataset.value;

        if (texts[section] && texts[section][value]) {
            if (value === "submit-btn" || value === "Register") {
                textToChange.value = texts[section][value];
            } else if (value === "email") {
                const emailInput = document.querySelector("input[type='email']");
                if (emailInput) {
                    emailInput.placeholder = texts[section][value];
                }
            } else if (value === "passwords") {
                const passwordInput = document.querySelector("input[type='password']");
                if (passwordInput) {
                    passwordInput.placeholder = texts[section][value];
                }
            } else if (value === "registroc") {
                const anchor = document.querySelector("a[data-value='registroc']");
                if (anchor) {
                    anchor.innerHTML = texts[section][value];
                }
            } else {
                textToChange.textContent = texts[section][value];
            }
        } else {
            console.log(`Translation not found for ${section} ${value}`);
        }
    }
}

flagsElement.addEventListener('click', (e) => {
    const lang = e.target.parentElement.dataset.language;
    changeLanguage(lang);
});

// Initial language load (you can adjust this based on your default language)
window.addEventListener("DOMContentLoaded", () => {
    const textsToChange = document.querySelectorAll("[data-section]");
    changeLanguage("es", textsToChange); // Set initial language to Spanish
});
