import os, random
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, jsonify, flash  # 👈 agrega flash
)

from flask_bcrypt import Bcrypt
from server.db import (
    crear_tabla_usuarios, agregar_usuario,
    obtener_usuario_por_email, obtener_usuario_por_id,
    crear_tabla_carrito, agregar_al_carrito,
    obtener_carrito_usuario, actualizar_cantidad_carrito,
    vaciar_carrito_usuario,
    agregar_al_carrito_personalizado,
    actualizar_usuario,  
    crear_tabla_contacto,
    guardar_contacto  
)


AVATARES_BIENVENIDA = ["img/persona1.png", "img/persona2.png", "img/persona3.png"]

app = Flask(__name__, template_folder='client/templates')
app.secret_key = os.environ.get('SECRET_KEY', 'una_clave_de_desarrollo_insegura')
bcrypt = Bcrypt(app)
crear_tabla_usuarios()
crear_tabla_carrito()
crear_tabla_contacto() 

@app.context_processor
def inject_cart_count():
    user_id = session.get('user_id')
    cart_count = 0
    if user_id:
        filas = obtener_carrito_usuario(user_id)
        cart_count = sum(f["cantidad"] for f in filas)
    return dict(cart_count=cart_count)

PRODUCTOS = {
    # ---------- Catálogo estándar ----------
    "bar":   {"slug": "bar",   "nombre": "Bar",   "precio": 250, "imagen": "img/bar.png"},
    "banos": {"slug": "banos", "nombre": "Baños", "precio": 260, "imagen": "img/banos.png"},
    "open":  {"slug": "open",  "nombre": "Open",  "precio": 280, "imagen": "img/open.png"},
    "closed":{"slug": "closed","nombre": "Closed","precio": 280, "imagen": "img/closed.png"},
    "twich": {"slug": "twich", "nombre": "Twich", "precio": 300, "imagen": "img/twich.png"},
    "exit":  {"slug": "exit",  "nombre": "Exit",  "precio": 300, "imagen": "img/exit.png"},

    # ---------- Catálogo personalizado ----------
    "palabras": {
        "slug": "palabras",
        "nombre": "Palabras",
        "precio": 100,  # puedes ajustar
        "imagen": "img/salaPlantilla.png"
    },
    "numeros": {
        "slug": "numeros",
        "nombre": "Números",
        "precio": 100,
        "imagen": "img/salaPlantillaNumeros.png"
    },
    "emoji": {
        "slug": "emoji",
        "nombre": "Emoji",
        "precio": 100,
        "imagen": "img/salaPlantillaEmoji.png"
    },
    "peliculas": {
        "slug": "peliculas",
        "nombre": "Películas",
        "precio": 100,
        "imagen": "img/salaPlantillaPulp.png"
    },
    "videojuegos": {
        "slug": "videojuegos",
        "nombre": "Videojuegos",
        "precio": 100,
        "imagen": "img/salaPlantillaMario.png"
    },
    "animes": {
        "slug": "animes",
        "nombre": "Animes",
        "precio": 100,
        "imagen": "img/salaPlantillaOne.png"
    },
}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.full_path))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        mensaje = request.form.get('mensaje', '').strip()

        # Validación simple
        if not nombre or not email or not mensaje:
            flash("Por favor completa todos los campos.", "error")
            # Volvemos a pintar el formulario con lo que ya escribió
            return render_template(
                'contact.html',
                nombre=nombre,
                email=email,
                mensaje=mensaje
            )

        # Guardar en BD
        guardar_contacto(nombre, email, mensaje)

        flash("¡Gracias por contactarnos! Te responderemos pronto.", "success")
        return redirect(url_for('contact'))

    # GET normal
    return render_template('contact.html')



# ============= RUTAS NUEVAS PARA VENTA PERSONAL =============

@app.route('/venta-personal')
def venta_personal():
    # aquí usas tu nuevo template ventaPersonal.html
    return render_template('ventaPersonal.html', productos=PRODUCTOS.values())

@app.route('/detalles-personal/<producto>')
def detallesP1(producto):
    p = PRODUCTOS.get(producto)
    if not p:
        return redirect(url_for('venta_personal'))  # o 'venta' si prefieres
    return render_template('detallesP1.html', producto=p)

# ---------- Agregar al carrito (estándar + personalizados) ----------
@app.route('/agregar/<producto_slug>', methods=['POST'])
@login_required
def agregar(producto_slug):
    try:
        p = PRODUCTOS.get(producto_slug)
        if not p:
            return jsonify({"ok": False, "error": "Producto no encontrado"}), 404

        # Soportar JSON o form-data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        # Extraer campos
        qty = int(data.get('qty', 1) or 1)
        size = data.get('size') or data.get('medida') or ''
        color = data.get('color') or ''
        custom_text = data.get('custom_text') or ''
        notes = data.get('notes') or ''
        action = data.get('action') or 'add'

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"ok": False, "error": "Usuario no autenticado"}), 401

        # Si trae texto/medida/color, tratamos como personalizado
        if custom_text or size or color or notes:
            agregar_al_carrito_personalizado(
                user_id=user_id,
                producto_slug=producto_slug,
                cantidad=qty,
                custom_text=custom_text,
                size=size,
                color=color,
                notes=notes
            )
        else:
            # caso simple: catálogo estándar (usa tu función normal)
            agregar_al_carrito(
                user_id=user_id,
                producto_slug=producto_slug,
                cantidad=qty,
                medida=size or 'default'
            )

        filas = obtener_carrito_usuario(user_id)
        cart_count = sum(int(f.get("cantidad", 1)) for f in filas)

        return jsonify({
            "ok": True,
            "cart_count": cart_count,
            "message": "Producto agregado al carrito"
        })

    except Exception as e:
        app.logger.exception("Error en /agregar")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/carrito')
@login_required
def carrito():
    user_id = session.get('user_id')
    filas = obtener_carrito_usuario(user_id)

    items = []
    total = 0

    for fila in filas:
        slug = fila['producto_slug']
        qty  = fila['cantidad']

        prod = PRODUCTOS.get(slug)
        if not prod:
            # Si el producto ya no existe en el catálogo, lo saltamos
            continue

        subtotal = prod['precio'] * qty
        total += subtotal

        medida      = fila.get('medida') or ''
        custom_text = fila.get('custom_text') or ''
        raw_color   = fila.get('color') or ''
        notes       = fila.get('notes') or ''

        # raw_color puede venir como: "#0044ff|||img/bar1.png"
        color = raw_color
        variant_img = None

        if '|||' in raw_color:
            color, variant_img = raw_color.split('|||', 1)
            color = color.strip()
            variant_img = variant_img.strip()

        detalles = []
        if custom_text:
            detalles.append(f'"{custom_text}"')
        if medida:
            detalles.append(f"Medida: {medida}")
        if color:
            detalles.append(f"Color: {color}")
        if notes:
            detalles.append(f"Notas: {notes}")

        # Si hay imagen de variante, úsala; si no, la imagen base del producto
        imagen_final = variant_img or prod['imagen']

        items.append({
            'slug': slug,
            'nombre': prod['nombre'],
            'precio': prod['precio'],
            'qty': qty,
            'subtotal': subtotal,
            'imagen': imagen_final,
            'detalles': " · ".join(detalles)
        })

    return render_template('carrito.html', items=items, total=total)


@app.route('/detalles/<producto>')
def detalles(producto):
    p = PRODUCTOS.get(producto)
    if not p:
        return redirect(url_for('venta'))
    return render_template('detalles1.html', producto=p)

@app.route('/venta')
def venta():
    return render_template('venta.html', productos=PRODUCTOS.values())


# ---------- Auth ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    if request.method == 'POST':
        fname = request.form['fname']
        lastname = request.form.get('lastname','')
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['cpassword']
        if password != confirm_password:
            return render_template('signup.html', error="Error: Las contraseñas no coinciden.")
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = agregar_usuario(fname, lastname, email, password_hash)
        if user_id:
            return redirect(url_for('login'))
        else:
            return render_template('signup.html', error="Error al registrar usuario. El email ya existe.")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home'))

    next_url = request.args.get('next') or request.form.get('next') or ''

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = obtener_usuario_por_email(email)
        if usuario and bcrypt.check_password_hash(usuario['password'], password):
            session['logged_in'] = True
            session['user_id'] = usuario['id']
            session['user_email'] = usuario['email']
            session['avatar_bienvenida'] = random.choice(AVATARES_BIENVENIDA)

            if next_url in ('None', 'null', 'undefined'):
                next_url = ''
            if next_url and not next_url.startswith('/'):
                next_url = ''

            return redirect(next_url or url_for('home'))
        else:
            return render_template('login.html', error="Contraseña o email incorrectos.", next=next_url)

    return render_template('login.html', next=next_url)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------- Home / Settings ----------
@app.route('/')
def home():
    if session.get('logged_in'):
        user_id = session.get('user_id')
        user_data = obtener_usuario_por_id(user_id)
        avatar = session.get('avatar_bienvenida')
        return render_template('auth/home.html', user=user_data, avatar=avatar)
    return render_template('index.html')

@app.route('/settings')
@login_required
def settings():
    user_id = session.get('user_id')
    user_data = obtener_usuario_por_id(user_id)
    return render_template('auth/settings.html', user=user_data)

    
@app.route('/carrito/vaciar', methods=['POST'])
@login_required
def vaciar_carrito():
    user_id = session.get('user_id')
    vaciar_carrito_usuario(user_id)
    return redirect(url_for('carrito'))

@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    user_id = session["user_id"]

    # Obtener datos del formulario
    fname = request.form.get("fname", "").strip()
    lastname = request.form.get("lastname", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()  # puede estar vacío

    # Si la contraseña está vacía, no la cambiamos
    if password:
        # 👇 Usa SIEMPRE bcrypt, igual que en /signup
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    else:
        password_hash = None

    # Llamamos a una función del módulo server.db
    actualizar_usuario(
        user_id=user_id,
        fname=fname,
        lastname=lastname,
        email=email,
        password_hash=password_hash
    )

    # Si cambió el email, actualizamos la sesión
    session["user_email"] = email

    flash("Perfil actualizado correctamente.", "success")
    return redirect(url_for("settings"))

if __name__ == '__main__':
    app.run(debug=True)
