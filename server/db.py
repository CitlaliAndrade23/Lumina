# server/db.py
import mysql.connector
from mysql.connector import errorcode

# Configuración de la conexión MySQL
db_config = {
    'user': 'root',
    'password': 'bebeosito777',
    'host': 'localhost',
    'database': 'prueba'
}

# ===================== TABLA USERS =====================

def crear_tabla_usuarios():
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        crear_tabla = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fname VARCHAR(50) NOT NULL,
            lastname VARCHAR(50),
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        """
        cursor.execute(crear_tabla)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Tabla 'users' creada o ya existe.")
    except mysql.connector.Error as err:
        print("Error al crear la tabla users:", err)

# ===================== TABLA CARRITO =====================
def crear_tabla_carrito():
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        crear_tabla = """
        CREATE TABLE IF NOT EXISTS carrito (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            producto_slug VARCHAR(50) NOT NULL,
            medida VARCHAR(50) NOT NULL,
            cantidad INT NOT NULL DEFAULT 1,
            custom_text VARCHAR(255) NULL,
            color VARCHAR(50) NULL,
            notes VARCHAR(255) NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY uniq_user_producto_medida (user_id, producto_slug, medida),
            CONSTRAINT fk_carrito_usuario
                FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
        cursor.execute(crear_tabla)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Tabla 'carrito' creada o ya existe.")
    except mysql.connector.Error as err:
        print("Error al crear la tabla carrito:", err)



def agregar_al_carrito(user_id, producto_slug, medida, cantidad):
    """Inserta o suma cantidad a un producto+medida en el carrito del usuario."""
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        sql = """
        INSERT INTO carrito (user_id, producto_slug, medida, cantidad)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE cantidad = cantidad + VALUES(cantidad)
        """
        cursor.execute(sql, (user_id, producto_slug, medida, cantidad))
        cnx.commit()
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print("Error al agregar al carrito:", err)

def agregar_al_carrito_personalizado(user_id, producto_slug, cantidad,
                                     custom_text, size, color, notes):
    """
    Inserta o actualiza un producto personalizado en el carrito.
    'size' se guarda en la columna 'medida'.
    """
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        query = """
        INSERT INTO carrito (user_id, producto_slug, medida, cantidad, custom_text, color, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            cantidad    = cantidad + VALUES(cantidad),
            custom_text = VALUES(custom_text),
            color       = VALUES(color),
            notes       = VALUES(notes)
        """
        cursor.execute(query, (
            user_id, producto_slug, size, cantidad,
            custom_text, color, notes
        ))

        cnx.commit()
        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        print("❌ Error al agregar carrito personalizado:", err)
        raise


def obtener_carrito_usuario(user_id):
    """Devuelve info del carrito del usuario."""
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT producto_slug,
                   medida,
                   cantidad,
                   custom_text,
                   color,
                   notes
            FROM carrito
            WHERE user_id = %s
            """,
            (user_id,)
        )
        filas = cursor.fetchall()
        cursor.close()
        cnx.close()
        return filas
    except mysql.connector.Error as err:
        print("Error al obtener carrito:", err)
        return []


def actualizar_cantidad_carrito(user_id, producto_slug, cantidad):
    """Actualiza la cantidad; si cantidad <= 0, elimina el producto."""
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        if cantidad <= 0:
            cursor.execute(
                "DELETE FROM carrito WHERE user_id = %s AND producto_slug = %s",
                (user_id, producto_slug)
            )
        else:
            cursor.execute(
                "UPDATE carrito SET cantidad = %s WHERE user_id = %s AND producto_slug = %s",
                (cantidad, user_id, producto_slug)
            )
        cnx.commit()
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print("Error al actualizar cantidad del carrito:", err)


def vaciar_carrito_usuario(user_id):
    """Vacía todo el carrito del usuario."""
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM carrito WHERE user_id = %s", (user_id,))
        cnx.commit()
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print("Error al vaciar carrito:", err)

# ===================== USUARIOS (CRUD) =====================

def agregar_usuario(fname, lastname, email, password_hash):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        insertar_usuario = """
        INSERT INTO users (fname, lastname, email, password)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insertar_usuario, (fname, lastname, email, password_hash))
        cnx.commit()
        last_id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return last_id
    except mysql.connector.Error as err:
        print("Error al agregar usuario:", err)
        return None


def obtener_usuario_por_email(email):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        cnx.close()
        return usuario
    except mysql.connector.Error as err:
        print("Error al obtener usuario:", err)
        return None


def obtener_usuario_por_id(user_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, fname, lastname, email FROM users WHERE id = %s",
            (user_id,)
        )
        usuario = cursor.fetchone()
        cursor.close()
        cnx.close()
        return usuario
    except mysql.connector.Error as err:
        print("Error al obtener usuario por ID:", err)
        return None

def actualizar_usuario(user_id, fname, lastname, email, password_hash=None):
    """
    Actualiza los datos del usuario. Si password_hash es None,
    no se modifica la contraseña.
    """
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        if password_hash:
            sql = """
                UPDATE users
                SET fname = %s,
                    lastname = %s,
                    email = %s,
                    password = %s
                WHERE id = %s
            """
            values = (fname, lastname, email, password_hash, user_id)
        else:
            sql = """
                UPDATE users
                SET fname = %s,
                    lastname = %s,
                    email = %s
                WHERE id = %s
            """
            values = (fname, lastname, email, user_id)

        cursor.execute(sql, values)
        cnx.commit()

        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print("Error al actualizar usuario:", err)

def crear_tabla_contacto():
    """Crea la tabla para mensajes de contacto si no existe."""
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS contacto (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            mensaje TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Tabla 'contacto' creada o ya existe.")
    except mysql.connector.Error as err:
        print("Error al crear tabla contacto:", err)


def guardar_contacto(nombre, email, mensaje):
    """Inserta un mensaje de contacto en la BD."""
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        sql = """
        INSERT INTO contacto (nombre, email, mensaje)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (nombre, email, mensaje))
        cnx.commit()
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print("Error al guardar contacto:", err)


