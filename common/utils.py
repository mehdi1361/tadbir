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


def type_check(correct_type):
    def check(old_function):
        def new_function(arg):
            if isinstance(arg, correct_type):
                return old_function(arg)
            else:
                print("Bad Type")
        return new_function
    return check

def normalize_data(value):
    dict_val = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9'
    }
    result_value = ""
    for char in value:
        if char in dict_val.keys():
            result_value += dict_val[char]

        else:
            result_value += char

    return result_value

