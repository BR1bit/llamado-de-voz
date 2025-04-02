from flask import Flask, render_template, redirect, url_for, request, session, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from datetime import datetime
import os


# Configuración de la app
app = Flask(__name__)
app.secret_key = 'ColCand2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/contactos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos
class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.String(255), nullable=True)

class RegistroAnuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# Rutas
@app.route('/')
def index():
    reproducir = os.path.exists("static/anuncio.mp3")
    ultimo_archivo = 'ultimo.txt'
    timestamp = None

    if reproducir:
        if os.path.exists(ultimo_archivo):
            with open(ultimo_archivo, 'r') as f:
                timestamp = f.read().strip()

    return render_template('index.html', reproducir=reproducir, timestamp=timestamp)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if usuario == 'admin' and contrasena == 'admin':
            session['usuario'] = usuario
            return redirect(url_for('contactos'))
        else:
            return render_template('login.html', error='Credenciales inválidas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

@app.route('/contactos')
def contactos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    buscar = request.args.get('buscar', '')
    if buscar:
        contactos = Contacto.query.filter(Contacto.nombre.ilike(f"%{buscar}%")).all()
    else:
        contactos = Contacto.query.all()
    return render_template('contactos.html', contactos=contactos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        telefono = request.form['telefono']
        nombre = request.form['nombre']
        mensaje = request.form.get('mensaje', '')
        nuevo = Contacto(telefono=telefono, nombre=nombre, mensaje=mensaje)
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('contactos'))
    return render_template('formulario.html', accion='Agregar')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])

def editar(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    contacto = Contacto.query.get_or_404(id)
    if request.method == 'POST':
        contacto.telefono = request.form['telefono']
        contacto.nombre = request.form['nombre']
        contacto.mensaje = request.form.get('mensaje', '')
        db.session.commit()
        return redirect(url_for('contactos'))
    return render_template('formulario.html', contacto=contacto, accion='Editar')

@app.route('/borrar/<int:id>')
def borrar(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    contacto = Contacto.query.get_or_404(id)
    db.session.delete(contacto)
    db.session.commit()
    return redirect(url_for('contactos'))

@app.route('/descargar')
def descargar():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    datos = Contacto.query.all()
    registros = [{'Teléfono': c.telefono, 'Nombre': c.nombre} for c in datos]
    df = pd.DataFrame(registros)
    archivo = 'registro_llegadas.xlsx'
    df.to_excel(archivo, index=False)
    return send_file(archivo, as_attachment=True)

# ✅ Esta es la función que necesitás para el main.py
def run_app():
    with app.app_context():
        os.makedirs("data", exist_ok=True)
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    
@app.route('/reproducido', methods=['POST'])
def reproducido():
    try:
        with open("static/ultimo.txt", "r") as f:
            archivo = f.read().strip()
        if archivo and os.path.exists(archivo):
            os.remove(archivo)
            print(f"🗑️ Archivo eliminado: {archivo}")
        if os.path.exists("static/ultimo.txt"):
            os.remove("static/ultimo.txt")
    except Exception as e:
        print(f"❌ Error al eliminar: {e}")
    return '', 204
    
@app.route('/registro')
def registro():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    anuncios = RegistroAnuncio.query.order_by(RegistroAnuncio.fecha.desc()).all()
    return render_template('registro.html', anuncios=anuncios)

import bot