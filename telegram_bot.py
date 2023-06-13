import logging
import os
import random
from logging.handlers import TimedRotatingFileHandler

import redis

from environs import Env
from telegram import ReplyKeyboardMarkup
from telegram.ext import Filters
from telegram.ext import Updater, MessageHandler

from create_intent import load_questions_answers

bot_logger = logging.getLogger(__file__)


def handle_message(update, context, questions_answers, redis_client):
    message = update.message
    chat_id = message.chat_id
    text = message.text

    if text == 'Новый вопрос':
        question = random.choice(list(questions_answers.keys()))

        redis_client.set(chat_id, question)

        context.bot.send_message(
            chat_id=chat_id,
            text=f'Вопрос: {question}'
        )

    elif text.startswith('Ответ:'):
        user_answer = text.split(':')[1].strip()

        previous_question_bytes = redis_client.get(chat_id)
        if previous_question_bytes is not None:
            previous_question = previous_question_bytes.decode()

            correct_answer = questions_answers.get(previous_question)

            if user_answer.lower() == correct_answer.lower():
                context.bot.send_message(
                    chat_id=chat_id,
                    text='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
                )
            else:
                context.bot.send_message(
                    chat_id=chat_id,
                    text='Неправильно… Попробуешь ещё раз?'
                )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text='Не найден предыдущий вопрос для проверки ответа.'
            )

    else:
        custom_keyboard = [['Новый вопрос', 'Сдаться'],
                           ['Мой счёт']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text='Custom Keyboard Test',
            reply_markup=reply_markup
        )



def main():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_file = os.path.join('logs', 'telegram_bot.log')
    file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    bot_logger.setLevel(logging.DEBUG)
    bot_logger.addHandler(file_handler)

    env = Env()
    env.read_env()

    telegram_token = env.str('TELEGRAM_TOKEN')
    quiz_files_folder = env.str('QUIZ_FILES_FOLDER')
    questions_answers = load_questions_answers(quiz_files_folder)

    redis_client = redis.Redis.from_url(env.str('REDIS_URL'))


    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(
        Filters.text & (~Filters.command),
        lambda update, context: handle_message(update, context, questions_answers, redis_client)
    ))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
