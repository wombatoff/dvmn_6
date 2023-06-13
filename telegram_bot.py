import logging
import os
import random
from enum import Enum
from functools import partial
from logging.handlers import TimedRotatingFileHandler

import redis
from environs import Env
from telegram import ReplyKeyboardMarkup
from telegram.ext import Filters, ConversationHandler, CommandHandler
from telegram.ext import Updater, MessageHandler

from create_intent import load_questions_answers

bot_logger = logging.getLogger(__file__)


class BotState(Enum):
    START = 1
    NEW_QUESTION = 2
    CHECK_ANSWER = 3


def handle_start(update, context):

    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите вариант:",
        reply_markup=reply_markup
    )
    return BotState.NEW_QUESTION


def handle_new_question(update, context):
    questions_answers = context.dispatcher.user_data['questions_answers']
    redis_client = context.dispatcher.user_data['redis_client']

    context.user_data['questions_answers'] = questions_answers
    context.user_data['redis_client'] = redis_client

    question = random.choice(list(questions_answers.keys()))

    context.user_data['current_question'] = question

    chat_id = update.message.chat_id
    redis_client.set(f"question:{chat_id}", question)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Вопрос: {question}"
    )

    return BotState.CHECK_ANSWER


def handle_check_answer(update, context):
    redis_client = context.dispatcher.user_data['redis_client']

    chat_id = update.message.chat_id
    current_question = redis_client.get(f"question:{chat_id}").decode('utf-8')

    correct_answer = context.user_data['questions_answers'][current_question]
    user_message = update.message.text
    if "Ответ:" in user_message:
        user_answer = user_message.split("Ответ:")[1].strip()
    else:
        user_answer = user_message

    if user_answer.lower() == correct_answer.lower():
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»."
        )
        redis_client.incr(f"correct_answers:{chat_id}")
        reply_markup = ReplyKeyboardMarkup([['Новый вопрос', 'Сдаться'], ['Мой счет']],
                                           one_time_keyboard=True)
        update.message.reply_text('Выберите действие:', reply_markup=reply_markup)
        return BotState.NEW_QUESTION

    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Неправильно... Попробуешь ещё раз?"
        )
        return BotState.CHECK_ANSWER


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
    updater = Updater(token=telegram_token, use_context=True)

    quiz_files_folder = env.str('QUIZ_FILES_FOLDER')
    questions_answers = load_questions_answers(quiz_files_folder)

    redis_client = redis.Redis.from_url(env.str('REDIS_URL'))

    updater.dispatcher.user_data['redis_client'] = redis_client
    updater.dispatcher.user_data['questions_answers'] = questions_answers

    start_handler = CommandHandler('start', handle_start)

    conversation_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            BotState.START:  [MessageHandler(Filters.text & ~Filters.command, handle_start)],
            BotState.NEW_QUESTION: [MessageHandler(Filters.text & ~Filters.command, handle_new_question)],
            BotState.CHECK_ANSWER: [MessageHandler(Filters.text & ~Filters.command, handle_check_answer)],
        },
        fallbacks=[start_handler]
    )
    updater.dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
