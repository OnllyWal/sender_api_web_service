class Email:
    def __init__(self, sender_name: str, complete_name: str, email_name: str, body: str, attachments: list, subject: str):
        """Inicializa o objeto Email com os parâmetros fornecidos."""
        self.sender_name = sender_name
        self.complete_name = complete_name
        self.email_name = email_name
        self.body = body
        self.attachments = attachments
        self.subject = subject


    def __repr__(self):
        """Representação textual do objeto Email."""
        return (f"Email(sender_name={self.sender_name}, complete_name={self.complete_name}, "
                f"email_name={self.email_name}, body={self.body[:30]}..., "
                f"attachments={len(self.attachments)} attachments)")