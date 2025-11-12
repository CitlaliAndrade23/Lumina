import random
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from server.db import crear_tabla_usuarios, agregar_usuario, obtener_usuario_por_email, obtener_usuario_por_id

AVATARES_BIENVENIDA = [
    "img/persona1.png",
    "img/persona2.png",
    "img/persona3.png",
]


# --- Configuración Inicial ---
app = Flask(__name__, template_folder='client/templates')
# CLAVE SECRETA: NECESARIA PARA CIFRAR LAS COOKIES DE SESIÓN
app.secret_key = os.environ.get('SECRET_KEY', 'una_clave_de_desarrollo_insegura') 
bcrypt = Bcrypt(app)
# Ejecutamos la creación de la tabla al inicio (si no existe)
crear_tabla_usuarios() 

# 🔹 AQUÍ DEFINIMOS LOS PRODUCTOS (ANTES DE LAS RUTAS)
PRODUCTOS = {
    "bar": {
        "slug": "bar",
        "nombre": "Bar",
        "precio": 250,
        "imagen": "img/bar.png"
    },
    "banos": {
        "slug": "banos",
        "nombre": "Baños",
        "precio": 260,
        "imagen": "img/banos.png"
    },
    "open": {
        "slug": "open",
        "nombre": "Open",
        "precio": 280,
        "imagen": "img/open.png"
    },
    "closed": {
        "slug": "closed",
        "nombre": "Closed",
        "precio": 280,
        "imagen": "img/closed.png"
    },
    "twich": {
        "slug": "twich",
        "nombre": "Twich",
        "precio": 300,
        "imagen": "img/twich.png"
    },
    "exit": {
        "slug": "exit",
        "nombre": "Exit",
        "precio": 300,
        "imagen": "img/exit.png"
    },
}



# --- Decorador de Autenticación (Middleware) ---
def login_required(f):
    """Decorador para restringir el acceso si no hay sesión activa."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            # Si no hay sesión, redirige al login
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Rutas Públicas (Enrutamiento Estático) ---

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/detalles/<producto>')
def detalles(producto):
    return render_template('detalles1.html', producto=producto)



@app.route('/venta')
def venta():
    return render_template('venta.html')


# --- Rutas de Autenticación (Login/Signup) ---

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Si el usuario ya está logueado, redirigir a Home Protegido (/)
    if session.get('logged_in'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        fname = request.form['fname']
        lastname = request.form.get('lastname','')
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['cpassword']

        # 1. Validación de Confirmación
        if password != confirm_password:
            return render_template('signup.html', error="Error: Las contraseñas no coinciden.")

        # 2. Cifrar la contraseña con Bcrypt
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # 3. Guardar el usuario en la DB
        user_id = agregar_usuario(fname, lastname, email, password_hash)
        
        if user_id:
            # Registro exitoso: redirige al login
            return redirect(url_for('login'))
        else:
            # Error de registro (ej. email duplicado)
            return render_template('signup.html', error="Error al registrar usuario. El email ya existe.")
            
    # Muestra el formulario GET
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está logueado, redirigir a Home Protegido (/)
    if session.get('logged_in'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        usuario = obtener_usuario_por_email(email)
        
        if usuario:
            # 1. Verificar la contraseña con Bcrypt
            if bcrypt.check_password_hash(usuario['password'], password):
                # 2. Éxito: Establecer la sesión de Flask
                session['logged_in'] = True
                session['user_id'] = usuario['id']
                session['user_email'] = usuario['email']

                # Elegimos un avatar de los 3 que hay para que de la bienvenida al nuestro usuario
                session['avatar_bienvenida'] = random.choice(AVATARES_BIENVENIDA)
                
                # 3. Redirigir al Home Protegido
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error="Contraseña o email incorrectos.")
        else:
            return render_template('login.html', error="Contraseña o email incorrectos.")
            
    # Muestra el formulario GET
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Cierra la sesión (elimina todas las claves)
    session.clear()
    # Redirige al login
    return redirect(url_for('login'))


# --- Rutas Protegidas y Dinámicas ---

@app.route('/')
def home():
    # 1. Verificar si la sesión está abierta
    if session.get('logged_in'):
        # SESIÓN ABIERTA: Mostrar contenido privado (home.html)
        user_id = session.get('user_id')
        user_data = obtener_usuario_por_id(user_id)

       # aqui estamos Recuperamos el avatar elegido al iniciar sesión
        avatar = session.get('avatar_bienvenida')
        
        #aqui estamos Renderizando la vista de sesión y le pasamos avatar al azar
        return render_template('auth/home.html', user=user_data, avatar=avatar)
    else:
        # SESIÓN CERRADA: Mostrar contenido público (index.html)
        # Asumimos que index.html es la página pública de bienvenida
        return render_template('index.html')


@app.route('/settings')
@login_required 
def settings():
    user_id = session.get('user_id')
    user_data = obtener_usuario_por_id(user_id)
    
    # RENDERIZA LA NUEVA PLANTILLA DENTRO DE AUTH/
    return render_template('auth/settings.html', user=user_data)


# --- Inicio del Servidor ---
if __name__ == '__main__':
    app.run(debug=True)