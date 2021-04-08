from twilio.rest import Client
import smtplib


MAIL_PROVIDER_SMTP_ADDRESS = "smtp.gmail.com"
MY_EMAIL = 'pooihern.birthday.service@gmail.com'


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, account_sid, account_api, gmail_password):
        self.account_sid = account_sid
        self.account_api = account_api
        self.gmail_password = gmail_password

    def send_notification(self, message):
        client = Client(self.account_sid, self.account_api)
        client.messages.create(
            body=message,
            from_='+14807257966',
            to='+60146604392'
        )

    def send_emails(self, emails, message, link):
        with smtplib.SMTP(MAIL_PROVIDER_SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=self.gmail_password)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{link}".encode('utf-8')
                )
