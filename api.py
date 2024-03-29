

# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals
import time
# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Какие завтра пары?",
                "Что задали на завтра?",
                "Какая следующая пара?",
            ]
        }

        res['response']['text'] = 'Привет! Чем я могу помочь?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    res['response']['text'] = req['request']['original_utterance'].lower()
    return
    if req['request']['original_utterance'].lower() == "какие завтра пары?":
        res['response']['text'] = get_first_lessons()
        return


    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]
    return suggests

def get_first_lessons():
    daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    timetable = {
        0: "",
        1: "",
        2: "",
        3: "",
        4: "Pravo 9:45, Fizo 16:45",
        5: "",
        6: "",
    }
    return timetable[daysOfWeek.index(time.strftime("%a"))]
