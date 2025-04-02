# Usa una imagen base de Python
FROM python:3.10-slim

# Establece variables de entorno para evitar prompts
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea el directorio para el volumen persistente
RUN mkdir -p /data

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Monta el volumen persistente
VOLUME /data

# Expone el puerto para la aplicación web
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python3", "main.py"]

