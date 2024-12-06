from controllers.api_connector import get_emails,process_email, update_email
from services.sender import EmailSender
import time

def main():
    sender = EmailSender()
    sender.connect()

    # URL do endpoint Flask
    endpoint_url = "http://172.19.113.12:5000/emails"
    while True:
        print("Buscando emails do servidor Flask...")
        # Busca e processa os emails
        emails = get_emails(endpoint_url)
        if emails:
            for email in emails:
                if email['status'] == "Processado":
                    #print(email)
                    string = email['anexos']
                    email["anexos"] = string.strip("{}").split(",")
                    print(f"{len(emails)} emails recebidos. Processando...")
                    email, id = process_email(email, sender)
                    update_email(email, id)
            
        else:
            print("Nenhum email foi recebido.")
        time.sleep(60)

if __name__ == "__main__":
    main()