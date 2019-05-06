from flask import Flask, jsonify, request
from flask_sslify import SSLify
import requests
import re
from misc import tokens

telegram_token = tokens['telegram']
currconv_token = tokens['currconv']

URL = 'https://api.telegram.org/bot' + telegram_token + '/'

app = Flask(__name__)
sslify = SSLify(app)


def send_message(chat_id, text='custom text'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=answer)
    return response.json()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        response = request.get_json()
        chat_id = response['message']['chat']['id']
        text = response['message']['text']

        patternHi = '(п|П)ривет+'
        patternBye = '(п|П)ока+'
        if bool(re.search(patternHi, text.lower())):
            send_message(chat_id, 'Привет! Рад тебя видеть! Чтобы получить текущий биржевой ключ валюты, напиши ее код')
        elif bool(re.search(patternBye, text.lower())):
            send_message(chat_id, 'Ну ты заходи если чо')
        else:
            rate = get_rate(text.upper())
            send_message(chat_id, text=rate)

        return jsonify(response)

    return '<h3>flask telegram bot app</h3>'


def get_rate(currency):
    pair = currency + '_RUB'
    url = 'https://free.currconv.com/api/v7/convert?q=' + pair + '&compact=ultra&apiKey=' + currconv_token
    response = requests.get(url).json()
    if pair in response:
        return response[pair]
    else:
        return 'У меня нет данных. Попробуй другой код валюты'

if __name__ == '__main__':
    app.run()