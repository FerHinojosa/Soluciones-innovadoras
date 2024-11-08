import pandas as pd
import smtplib
import ssl
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno para proteger credenciales
load_dotenv()
SMTP_SERVER = "smtp.gmail.com"
PORT = 465  # Para SSL
SENDER_EMAIL = os.getenv("SENDER_EMAIL")  # Correo remitente
PASSWORD = os.getenv("EMAIL_PASSWORD")    # Contraseña segura desde variable de entorno

def leer_csv(ruta_csv):
    """
    Lee un archivo CSV y devuelve un DataFrame de pandas. Verifica columnas requeridas.
    """
    try:
        contactos = pd.read_csv(ruta_csv)
        columnas_requeridas = {'nombre', 'fecha_de_cumpleaños', 'correo_electronico', 'mensaje'}
        if not columnas_requeridas.issubset(contactos.columns):
            raise ValueError("El CSV no contiene las columnas necesarias.")
        contactos = contactos.dropna(subset=['correo_electronico', 'fecha_de_cumpleaños'])
        return contactos
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

def es_correo_valido(correo):
    """
    Verifica si el correo tiene un formato válido.
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", correo) is not None

def enviar_correo(destinatario, asunto, mensaje_html):
    """
    Envía un correo electrónico a un destinatario específico.
    """
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje_html, "html"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, destinatario, msg.as_string())
    except smtplib.SMTPException as e:
        print(f"Error al enviar el correo a {destinatario}: {e}")

def enviar_felicitaciones_cumple(ruta_csv):
    """
    Lee una lista de contactos desde un archivo CSV y envía un saludo de cumpleaños a cada uno.
    """
    contactos = leer_csv(ruta_csv)
    if contactos.empty:
        print("No se encontraron contactos para enviar correos.")
        return

    hoy = datetime.now().strftime("%Y-%m-%d")
    cumpleañeros = contactos[contactos['fecha_de_cumpleaños'] == hoy]

    for _, contacto in cumpleañeros.iterrows():
        destinatario = contacto['correo_electronico']
        nombre = contacto['nombre']
        mensaje = contacto['mensaje']

        # Validar correo y personalizar mensaje
        if es_correo_valido(destinatario):
            mensaje_html = f"""
            <html>
            <body>
                <h2>¡Feliz cumpleaños, {nombre}!</h2>
                <p>{mensaje}</p>
                <p>Saludos,<br>El equipo de Recursos Humanos</p>
            </body>
            </html>
            """
            try:
                enviar_correo(destinatario, "¡Saludos de cumpleaños!", mensaje_html)
                print(f"Correo enviado a {destinatario}")
            except Exception as e:
                print(f"Error al enviar a {destinatario}: {e}")
        else:
            print(f"Correo inválido: {destinatario}")

# Ejecuta el envío de felicitaciones si es el archivo principal
if __name__ == "__main__":
    ruta_csv = "contactos_cumpleaños.csv"  # Ruta del archivo CSV
    enviar_felicitaciones_cumple(ruta_csv)
