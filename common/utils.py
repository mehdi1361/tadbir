from django.conf import settings
from zeep import Client


class SmsSender(object):
    def __init__(self, to, text):
        self.to = to
        self.text = text

    def send(self):
        params = {
            "username": settings.SMS_SENDER_USERNAME,
            "password": settings.SMS_SENDER_PASSWORD,
            "from": settings.SMS_SENDER_FROM,
            "to": [self.to],
            "text": self.text,
            "udh": settings.SMS_SENDER_UDH,
            "isflash": settings.SMS_SENDER_IS_FLASH
        }

        client = Client(settings.SMS_SENDER_URL)
        result = client.service.SendSms(**params)
        return result
