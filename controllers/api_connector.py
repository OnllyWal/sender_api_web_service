import requests
import os
from models.email_model import Email
def get_emails(endpoint_url):
    try:
        # Faz a requisição GET para o endpoint Flask
        response = requests.get(endpoint_url)
        response.raise_for_status()  # Verifica se houve erro HTTP
        emails = response.json()  # Converte a resposta JSON para um objeto Python (lista de dicionários)
        return emails
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados do endpoint: {e}")
        return []
    

def download_files(files_path):
    try:
        n_path = []
        for path in files_path:
            path = path.replace("{", '').replace("}", '')
            response = requests.get(f"http://172.19.113.12:5000{path}", stream=True)
            if response.status_code  == 200:
                file_path = f"/home/wal/sender_api_web_service{path}"
                print("\n_________________________________________\n")
                if not os.path.exists("/home/wal/sender_api_web_service/download"):
                    os.makedirs(os.path.dirname(file_path))
                n_path.append(file_path)
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=81920):
                        file.write(chunk)
                        print(f"Arquivo {path}, baixado com sucesso!")

            else:
                print(f"Erro ao baixar o arquivo {path}:{response.status_code}")
        return n_path
    except Exception as e:
        print(f"Erro ao baixar o arquivo: {str(e)}")

def json_to_email(dados):
    email_obj = Email(
        sender_name= "Equipe",
        complete_name= "Equipe PPComp",
        email_name = "maquinas902@gmail.com",
        subject = "Documentos de Defesa",
        body = f"{dados['corpo']} \n\n Atenciosamente,\n Equipe PPComp",
        attachments=dados["anexos"]
        )
    return email_obj

def remove_docs(paths):
    for path in paths:
        try:
            os.remove(path)
        except Exception as e:
            print(f"Erro ao remover {path}: {str(e)}")

def process_email(email,sender):
    # Manipula os dados recebidos conforme a necessidade
    destinatario = "walcandeia@gmail.com"
    id = email['id']
    if email['tipo'] == "Defesa":
        files_path = email['anexos']
        print(files_path)
        email['anexos'] = download_files(files_path)
        print(email['anexos'])
    email_obj = json_to_email(email)
    sender.send_email(email_obj, destinatario)
    sender.send_email(email_obj, email['origin_address'])
    email['status'] = 'Enviado'

    return email, id

def update_email(email, id):
    response = requests.put(f"http://172.19.113.12:5000/emails/{id}", json=email)
    print(response.json)
    remove_docs(email['anexos'])
