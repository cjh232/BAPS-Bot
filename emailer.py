import smtplib
import secrets
from email.mime.text import MIMEText
from datetime import datetime


class Emailer:
    def __init__(self, sender, receiver, user, password, smtp_domain, smtp_port):
        self.user = user
        self.password = password
        self.sender = sender
        self.receiver = receiver
        self.messageQueue = []
        self.smtp_domain = smtp_domain
        self.smtp_port = smtp_port

    def appendMessage(self, match_object):

        # Convert the reddit post into a dictionary which will hold
        # the html formatting needed for the email.

        time_posted = datetime.fromtimestamp(match_object.created_utc)

        msg = {
            "title": f"<h2>{match_object.title}</h2>",
            "time_posted": f"<h3>Posted At: {time_posted}</h3>",
            "url": f'<a href="{match_object.url}">{match_object.url}</a>'
        }

        self.messageQueue.append(msg)


    def _stitchMessage(self):

        # Combine all the messages in the messageQueue into
        # a single string which will be sent via email.

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

        """Send email via SMTP sever.
        """

        body = self._stitchMessage()

        msg = MIMEText(body, 'html')

        now = datetime.now()
        current_datetime = now.strftime("%d/%m/%Y %H:%M:%S")

        msg['Subject'] = f'Build a PC Sales Bot - {current_datetime}'
        msg['From'] = self.sender
        msg['To'] = self.receiver

        with smtplib.SMTP(self.smtp_domain, self.smtp_port) as server:

            server.login(self.user, self.password)
            server.sendmail(self.sender, self.receiver, msg.as_string())
            print("Mail successfully sent")
