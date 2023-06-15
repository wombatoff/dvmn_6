import logging
import os
from logging.handlers import TimedRotatingFileHandler
import random

import redis
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from create_intent import load_questions_answers



bot_logger = logging.getLogger(__file__)


def handle_start(event, vk_api, questions_answers):
    user_id = event.user_id

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)

    vk_api.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Выберите вариант:'
    )


def handle_new_question(event, vk_api, redis_client, questions_answers):
    user_id = event.user_id

    question = random.choice(list(questions_answers.keys()))
    redis_client.set(f"question:{user_id}", question)

    vk_api.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        message=f"Вопрос: {question}"
    )


def handle_check_answer(event, vk_api, redis_client, questions_answers):
    user_id = event.user_id
    user_answer = event.text

    current_question = redis_client.get(f"question:{user_id}").decode('utf-8')

    if user_answer == "Сдаться":
        correct_answer = questions_answers[current_question]
        vk_api.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            message=f"Правильный ответ: {correct_answer}"
        )
        handle_new_question(event, vk_api, redis_client, questions_answers)
    else:
        correct_answer = questions_answers[current_question]
        if user_answer.lower() == correct_answer.lower():
            vk_api.messages.send(
                user_id=user_id,
                random_id=get_random_id(),
                message="Правильно! Поздравляю! Для следующего вопроса нажмите «Новый вопрос»."
            )
            redis_client.incr(f"correct_answers:{user_id}")
            handle_new_question(event, vk_api, redis_client, questions_answers)
        else:
            vk_api.messages.send(
                user_id=user_id,
                random_id=get_random_id(),
                message="Неправильно... Попробуйте ещё раз?"
            )


def main():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log_file = os.path.join("logs", "vk_bot.log")
    file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    bot_logger.setLevel(logging.DEBUG)
    bot_logger.addHandler(file_handler)

    env = Env()
    env.read_env()

    vk_token = env.str('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    quiz_files_folder = env.str('QUIZ_FILES_FOLDER')
    questions_answers = load_questions_answers(quiz_files_folder)

    redis_client = redis.Redis.from_url(env.str('REDIS_URL'))

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == "Начать":
                handle_start(event, vk_api, questions_answers)
            elif event.text == "Новый вопрос":
                handle_new_question(event, vk_api, redis_client, questions_answers)
            elif event.text == "Сдаться":
                handle_check_answer(event, vk_api, redis_client, questions_answers)


if __name__ == "__main__":
    main()
