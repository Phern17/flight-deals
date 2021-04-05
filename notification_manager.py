from twilio.rest import Client


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, account_sid, account_api):
        self.account_sid = account_sid
        self.account_api = account_api

    def send_notification(self, message):
        client = Client(self.account_sid, self.account_api)
        message = client.messages.create(
            body=f"Low Price alert! {message}",
            from_='+14807257966',
            to='+60146604392'
        )