import smtplib
import secrets
from email.mime.text import MIMEText
from datetime import datetime


class Emailer:
    def __init__(self, sender, receiver, user, password):
        self.user = user
        self.password = password
        self.sender = sender
        self.receiver = receiver
        self.messageQueue = []

    def appendMessage(self, message_object):

        time_posted = datetime.fromtimestamp(message_object.created_utc)

        msg = {
            "title": f"<h2>{message_object.title}</h2>",
            "time_posted": f"<h3>Posted At: {time_posted}</h3>",
            "url": f'<a href="{message_object.url}">{message_object.url}</a>'
        }

        self.messageQueue.append(msg)

    def _stitchMessage(self):
        body = ""

        for msg in self.messageQueue:
            body += msg["title"]
            body += msg["time_posted"]
            body += msg["url"]
            body += "<hr>"
        
        return body
    
    def getQueueLength(self):

        return len(self.messageQueue)

    def sendEmail(self):

        body = self._stitchMessage()

        msg = MIMEText(body, 'html')

        now = datetime.now()
        current_datetime = now.strftime("%d/%m/%Y %H:%M:%S")

        msg['Subject'] = f'Build a PC Sales Bot - {current_datetime}'
        msg['From'] = self.sender
        msg['To'] = self.receiver

        with smtplib.SMTP(secrets.smtp_domain, secrets.smtp_port) as server:

            server.login(self.user, self.password)
            server.sendmail(self.sender, self.receiver, msg.as_string())
            print("Mail successfully sent")

