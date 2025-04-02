from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecreto2025'  # Podés cambiarlo por uno más seguro en producción

# ✅ Base de datos persistente en volumen montado
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/contactos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de contacto
class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.String(255))