import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

class Notification:
    """
    A class for sending email notifications.

    Attributes:
        email_receiver (str): The email address that will receive the notifications.
        email_sender (str): The email address that will send the notifications. Default is set to a specific address.
        email_sender_pwd (str): The password for the sender's email account. Default is set to a placeholder.
        smtp_server (str): The SMTP server address. Default is set to Gmail's SMTP server.

    Methods:
        forward_email(subject, message): Send an email to the receiver with the given subject and message.
    """

    def __init__(
        self,
        email_receiver: str,
        email_sender: str = "bestucollege101@gmail.com",
        email_sender_pwd: str = "copz auen jwkm twzf",
        smtp_server: str = "smtp.gmail.com",
    ):
        self.email_sender = email_sender
        self.email_sender_pwd = email_sender_pwd
        self.smtp_server = smtp_server
        self.email_receiver = email_receiver

    
    def create_email_content(self, file_path: str, code: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_template = file.read()

        email_content = html_template.replace('{verify_code}', code)

        return email_content
    
    """
    Send an email to the receiver with the given subject and message.

    If an exception occurs, the method prints the exception message. 

    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.
    """

    def forward_email(self, subject: str, code: str) -> None:
        context = ssl.create_default_context()
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.email_sender
        msg['To'] = self.email_receiver

        # Attach image and HTML content
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the path to your file
        file_path = os.path.join(script_dir, 'bestyou_verify.html')
        
        html_content = self.create_email_content(file_path, code = code)

        msg.attach(MIMEText(html_content, 'html'))

        # Send the email
        try:
            with smtplib.SMTP(self.smtp_server, port=587) as server:
                server.starttls(context=context)
                server.login(user=self.email_sender, password=self.email_sender_pwd)
                server.sendmail(self.email_sender, self.email_receiver, msg.as_string())
        except Exception as e:
            print(f"Failed to send email: {e}")


def send_verification_code_email(email: str, code: str) -> None:
    notification_sys = Notification(
        email_sender="bestucollege101@gmail.com",
        email_sender_pwd="copz auen jwkm twzf",
        smtp_server="smtp.gmail.com",
        email_receiver=email
    )
    
    notification_sys.forward_email(subject="Your Verification Code", code = code)
        
        
if __name__ == "__main__":
    notification_sys = Notification(
        email_sender="bestucollege101@gmail.com",
        email_sender_pwd="copz auen jwkm twzf",
        smtp_server="smtp.gmail.com",
        email_receiver="gejin559@gmail.com"
    )

    message = """This message is sent from Here."""
    
    notification_sys.forward_email(subject="Your Verification Code", code = "362812")

