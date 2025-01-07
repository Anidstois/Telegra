# bot.py
import telebot
from extensions import CurrencyConverter, APIException
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Здравствуйте! Я бот для получения курса валют.\n"
                          "Введите запрос в формате:\n"
                          "<имя валюты, цену которой вы хотите узнать> <имя валюты, в которой нужно узнать цену> <количество валюты>\n"
                          "Пример: USD RUB 10\n\n"
                          "Используйте команду /values для получения списка доступных валют.")


@bot.message_handler(commands=['values'])
def send_values(message):
    bot.reply_to(message, "Доступные валюты: EUR, USD, RUB.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        text = message.text.split()
        if len(text) != 3:
            raise APIException("Неверный формат запроса. Пример: USD RUB 10")

        base, quote, amount = text
        amount = float(amount)

        # Получаем результат от CurrencyConverter
        total_amount = CurrencyConverter.get_price(base, quote, amount)

        # Ответ бота
        bot.reply_to(message, f"{amount} {base} = {total_amount} {quote}")

    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")
    except ValueError:
        bot.reply_to(message, "Количество валюты должно быть числом.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")


if __name__ == '__main__':
    bot.polling(none_stop=True)
