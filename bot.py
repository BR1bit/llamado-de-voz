from telegram import Update, Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from models_bot import app, db, Contacto
import asyncio, os
import edge_tts
from uuid import uuid4
from app import RegistroAnuncio 

TOKEN = "7857242658:AAFggJxdG-qzzmhauHHEfyJ5kqtal0AHqZA"

# Función para generar audio con edge_tts
async def anunciar_async(nombre):
    mensaje = nombre if "tu familia ha llegado" in nombre.lower() else f"{nombre}, tu familia ha llegado"
    archivo = f"static/anuncio_{uuid4().hex}.mp3"
    communicate = edge_tts.Communicate(text=mensaje, voice="es-AR-ElenaNeural")
    await communicate.save(archivo)
    with open("static/ultimo.txt", "w") as f:
        f.write(archivo)
    print(f"✅ Generado {archivo} con el mensaje: {mensaje}")

def anunciar(nombre):
    asyncio.run(anunciar_async(nombre))

# /start

def start(update: Update, context: CallbackContext):
    contacto_btn = KeyboardButton("📱 Compartir número", request_contact=True)
    teclado = ReplyKeyboardMarkup([[contacto_btn]], one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Hola 👋🏼 Tocá el botón para compartir tu número:", reply_markup=teclado)

# Contacto recibido
def recibir_contacto(update: Update, context: CallbackContext):
    contacto = update.message.contact
    numero = contacto.phone_number.replace("+", "").strip()
    print(f"📲 Número recibido: {numero}")
    
    with app.app_context():
        resultado = Contacto.query.filter_by(telefono=numero).first()
        if resultado:
            mensaje_a_reproducir = resultado.mensaje if resultado.mensaje else f"{resultado.nombre}, tu familia ha llegado"
            anunciar(mensaje_a_reproducir)

            # Registrar en historial
            registro = RegistroAnuncio(nombre=resultado.nombre)
            db.session.add(registro)
            db.session.commit()

            update.message.reply_text(f"✅ Se anunció: {resultado.nombre}")
        else:
            update.message.reply_text("❌ Tu número no está registrado. Consultá en Secretaría.")

# Función principal para correr el bot con polling
def run_polling():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.contact, recibir_contacto))

    print("🤖 Bot en modo polling...")
    updater.start_polling()
    updater.idle()
