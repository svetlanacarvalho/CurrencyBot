import requests
import json
from config import *

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не могу обработать валюту "{quote}"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не могу обработать валюту "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Что-то пошло не так. Я не могу обработать количество "{amount}". Попробуй ещё раз.')

        if quote == base:
            raise APIException(f'Здесь одинаковые валюты "{base}". Я не могу их перевести.')

        r = requests.request("GET",
                             f'https://api.apilayer.com/fixer/convert?to={base_ticker}&from={quote_ticker}&amount={amount}',
                             headers=headers)
        print(r)
        print(json.loads(r.content))
        text = json.loads(r.content)["result"]
        return round(text, 2)