FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los requerimientos e instalamos dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código fuente
COPY . /app/

# Comando por defecto al iniciar el contenedor
# Escucha en el puerto 8000 disponible para el mundo (0.0.0.0)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]