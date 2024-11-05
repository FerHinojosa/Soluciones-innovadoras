import pandas as pd
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración del servidor de correo
SMTP_SERVER = "smtp.gmail.com"
PORT = 465  # Para SSL
SENDER_EMAIL = "fernando.hinojosas@gmail.com"  # Reemplaza con tu dirección de correo electrónico
PASSWORD = "Test123456789"  # Reemplaza con tu contraseña


def leer_csv(ruta_csv):
    """
    Lee un archivo CSV y devuelve un DataFrame de pandas.

    Parameters:
        ruta_csv (str): La ruta del archivo CSV.

    Returns:
        pd.DataFrame: DataFrame que contiene los datos del archivo CSV.
    """
    return pd.read_csv(ruta_csv)


def enviar_correo(destinatario, mensaje):
    """
    Envía un correo electrónico a un destinatario específico.

    Parameters:
        destinatario (str): La dirección de correo electrónico del destinatario.
        mensaje (str): El mensaje a enviar en el correo.
    """
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = destinatario
    msg["Subject"] = "¡Saludos de cumpleaños!"

    # Agregar el cuerpo del mensaje al correo
    msg.attach(MIMEText(mensaje, "plain"))

    # Conectar al servidor SMTP y enviar el correo
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, destinatario, msg.as_string())


def enviar_saludos_desde_csv(ruta_csv):
    """
    Lee una lista de contactos desde un archivo CSV y envía un saludo a cada uno.

    Parameters:
        ruta_csv (str): La ruta del archivo CSV con los datos de los contactos.
    """
    contactos = leer_csv(ruta_csv)
    for _, contacto in contactos.iterrows():
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
    enviar_saludos_desde_csv(ruta_csv)
