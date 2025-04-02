import threading
import app
import bot

if __name__ == '__main__':
    print("🌐 Iniciando aplicación web...")
    t1 = threading.Thread(target=app.run_app)
    t1.start()

    print("🤖 Iniciando bot (polling)...")
    bot.run_polling()
