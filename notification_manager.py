import os
import smtplib


class NotificationManager:
    def __init__(self):
        self.my_gmail = "kobiljonkhayrullayev@gmail.com"
        self.my_yahoo = "qobiljonxayrullayev@yahoo.com"
        self.password = os.environ["password"]
        self.GMAIL_SMTP = "smtp.gmail.com"

    def send_message(self, message, user_email):
        with smtplib.SMTP(self.GMAIL_SMTP) as connection:
            connection.starttls()
            connection.login(self.my_gmail, password=self.password)
            connection.sendmail(from_addr=self.my_gmail, to_addrs=user_email, msg=f"Subject: Price Alert\n\n{message}")