import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from models.email_model import Email

class EmailSender:
    def __init__(self):
        self.email_address = "maquinas902@gmail.com"
        self.password = "vjmm jseq feuk amhv"
        self.connection = None

    def connect(self):
        '''Conecta ao servidor SMTP para enviar emails.'''
        self.connection = smtplib.SMTP('smtp.gmail.com', 587)
        self.connection.starttls()
        self.connection.login(self.email_address, self.password)
        print("Conectado ao servidor de envio")

    def send_email(self, email_obj: Email, destinatario: str):
        '''Envia um email a partir de um objeto Email e inclui o nome completo do remetente.'''
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = destinatario
        msg['Subject'] = email_obj.subject

        # Adiciona o corpo do email, incluindo o nome completo do aluno
        body_content = email_obj.body
        msg.attach(MIMEText(body_content, 'plain'))

        # Adiciona os anexos
        if email_obj.attachments:
            for attachment_path in email_obj.attachments:
                part = MIMEBase('application', 'vnd.openxmlformats-officedocument.wordprocessingml.document')
                
                try:
                    with open(attachment_path, 'rb') as attachment:
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        filename = os.path.basename(attachment_path)
                        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                        msg.attach(part)
                except Exception as e:
                    print("Erro ao Anexar")

        # Envia o email
        self.connection.sendmail(self.email_address, destinatario, msg.as_string())
        print(f"Email enviado para {destinatario}")

    def disconnect(self):
        '''Desconecta do servidor SMTP.'''
        if self.connection:
            self.connection.quit()