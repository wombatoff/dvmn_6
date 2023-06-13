import logging
import os
import random
from logging.handlers import TimedRotatingFileHandler

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

bot_logger = logging.getLogger(__file__)


def handle_message_vk(env, event, vk_api):
    try:
        session_id = event.user_id
        text = event.text
        language_code = 'ru'

        project_id = env.str('GOOGLE_PROJECT_ID')
        response_text = detect_intent_texts(env, project_id, session_id, text, language_code)

        if response_text and not response_text.intent.is_fallback:
            vk_api.messages.send(
                user_id=event.user_id,
                message=response_text.fulfillment_text,
                random_id=random.randint(1, 1000000)
            )
    except Exception as e:
        bot_logger.exception('An error occurred while handling the message')
        vk_api.messages.send(
            user_id=event.user_id,
            message='Произошла ошибка при обработке сообщения.',
            random_id=random.randint(1, 1000000)
        )


def main():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_file = os.path.join('logs', 'vk_bot.log')
    file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, encoding='utf-8')
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

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message_vk(env, event, vk_api)


if __name__ == '__main__':
    main()
