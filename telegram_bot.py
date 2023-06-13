import logging
import os
from logging.handlers import TimedRotatingFileHandler

from environs import Env
from telegram.ext import Filters
from telegram.ext import Updater, MessageHandler

from create_intent import load_questions_answers

bot_logger = logging.getLogger(__file__)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log_file = os.path.join("logs", "telegram_bot.log")
    file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    bot_logger.setLevel(logging.DEBUG)
    bot_logger.addHandler(file_handler)

    env = Env()
    env.read_env()

    telegram_token = env.str("TELEGRAM_TOKEN")
    quiz_files_folder = env.str('QUIZ_FILES_FOLDER')
    questions_answers = load_questions_answers(quiz_files_folder)

    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()


if __name__ == "__main__":
    main()
