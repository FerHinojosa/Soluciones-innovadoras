import pandas as pd
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuración del servidor de correo
SMTP_SERVER = "smtp.gmail.com"
PORT = 465  # Para SSL
SENDER_EMAIL = "tu_email@gmail.com"  # Reemplaza con tu dirección de correo electrónico
PASSWORD = "tu_contraseña"  # Reemplaza con tu contraseña

def leer_csv(ruta_csv):
    """
    Lee el archivo CSV y retorna un DataFrame.
    """
    return pd.read_csv(ruta_csv)

def enviar_correo(destinatario, mensaje):
    """
    Envía un correo electrónico al destinatario especificado.
    """
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = destinatario
    msg["Subject"] = "¡Feliz cumpleaños!"

    msg.attach(MIMEText(mensaje, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, destinatario, msg.as_string())

def enviar_felicitaciones_cumple(ruta_csv):
    """
    Verifica las fechas de cumpleaños y envía felicitaciones si coincide con la fecha actual.
    """
    hoy = datetime.now().strftime("%Y-%m-%d")
    contactos = leer_csv(ruta_csv)

    cumpleañeros = contactos[contactos['fecha_de_cumpleaños'] == hoy]
    
    for _, contacto in cumpleañeros.iterrows():
        destinatario = contacto['correo_electronico']
        mensaje = contacto['mensaje']
        
        try:
            enviar_correo(destinatario, mensaje)
            print(f"Correo enviado a {destinatario}")
        except Exception as e:
            print(f"Error al enviar a {destinatario}: {e}")

if __name__ == "__main__":
    # Ruta del archivo CSV
    ruta_csv = "contactos_cumpleaños.csv"
    enviar_felicitaciones_cumple(ruta_csv)
