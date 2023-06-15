# -*- coding: utf-8 -*-
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id


def main():
    """ Пример создания клавиатуры для отправки ботом """

    vk_session = vk_api.VkApi(token='vk1.a.QqOJARRspm-kigxgVl5hWym-6rx9_iJOypzx2P9LL7Bk7W72HwyN2kfKQnqgH01ySIMZy1XCZjrLniD_B2RGp-hYrmCgcSRCH7Wv1rhLs7rh2Yx_RqqiYzI1fs2PIaUe9MQhh5yIIk0y3xUW_tbKDwMWYoX8eRcInJHmBCWudmZfyZHwy03X-rxop9pUa_M5Xd0l1Uex79c_2za2sLDjOQ')
    vk = vk_session.get_api()

    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Белая кнопка', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)

    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button('Красная кнопка', color=VkKeyboardColor.NEGATIVE)

    keyboard.add_line()
    keyboard.add_button('Синяя кнопка', color=VkKeyboardColor.PRIMARY)

    vk.messages.send(
        peer_id=5835687,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Пример клавиатуры'
    )


if __name__ == '__main__':
    main()