# 🗣️ Llamado por Voz

Aplicación web + bot de Telegram que permite anunciar por parlantes cuando una familia llega a retirar a un estudiante, con generación de audio automática y administración desde un panel web.

## 🚀 Características

- 🎤 Generación de anuncios por voz con `edge-tts` (voz en español de Argentina)
- 🤖 Bot de Telegram para que las familias anuncien su llegada compartiendo su número
- 📄 Panel de administración (login requerido) para:
  - Ver, agregar, editar y borrar contactos
  - Buscar contactos por nombre
  - Personalizar el mensaje a reproducir
- 🎧 Reproducción automática del audio en el navegador (con botón para activarla)
- 🗑️ Borrado automático del audio una vez reproducido
- 📋 Historial de anuncios realizados
- 💾 Base de datos persistente usando volumen en Fly.io

## 🧑‍💻 Tecnologías

- Python 3.10
- Flask + SQLAlchemy
- edge-tts
- Telegram Bot API
- HTML + CSS (Jinja2)
- Fly.io (deploy)

## ⚙️ Instalación local (modo polling)

1. Cloná el repo:

```bash
git clone https://github.com/BR1bit/llamado-de-voz.git
cd llamado-de-voz
```

2. Instalá dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutá la app:

```bash
python main.py
```

---

## 📦 Estructura del proyecto

```
├── app.py              # Web + panel de administración
├── bot.py              # Bot de Telegram con polling
├── main.py             # Arranca app y bot
├── templates/          # HTMLs con Jinja2
├── static/             # Audios generados
├── data/               # Base de datos SQLite
└── fly.toml            # Configuración para Fly.io
```

---

## 🚗 Deploy en Fly.io

El proyecto se encuentra desplegado en:  
🌐 **https://proyecto-voz.fly.dev/**

---

## 🙌 Autor

Bruno — [@BR1bit](https://github.com/BR1bit)

---

## 📜 Licencia

MIT

