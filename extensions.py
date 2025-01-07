import requests
import json

class APIException(Exception):
    """Исключение для обработки ошибок API."""
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        """Получает цену на указанное количество валюты через API."""
        url = f"https://openexchangerates.org/api/latest.json?app_id=f6913d58d8ea4bb4a40d7d7bfcd3cba4&currencies=USD,RUB,EUR"

        try:
            response = requests.get(url)

            # Проверка успешности запроса
            if response.status_code != 200:
                raise APIException(f"Ошибка HTTP: код ответа {response.status_code}")

            data = response.json()

            # Проверка на наличие ошибки в ответе API
            if "error" in data:
                raise APIException(f"Ошибка API: {data['error']}")

            # Проверка наличия валюты в данных
            if quote not in data['rates']:
                raise APIException(f"Валюта {quote} не поддерживается API.")

            # Получаем курс валюты и вычисляем итоговую сумму
            rate = data['rates'][quote]
            total_amount = rate * amount
            return total_amount

        except requests.exceptions.RequestException as e:
            raise APIException(f"Ошибка при запросе к API: {str(e)}")

        except ValueError:
            raise APIException("Ошибка обработки данных: неверный формат ответа от API.")

        except KeyError:
            raise APIException("Ошибка в данных API: отсутствует необходимая информация.")
