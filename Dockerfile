FROM python:3.9-slim
WORKDIR /app
# Instalamos pandas y requests para el script
RUN pip install pandas
COPY sync_cameras.py .
# El script escribirá en /data, que es nuestro volumen
CMD ["python", "sync_cameras.py"]
