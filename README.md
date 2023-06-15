
# Проводим викторину
### Описание
Telegram и VK бот, который проводит викторину

### Стек технологий:
- Python
- python-telegram-bot
- vk_api
- Redis
---

## Запуск проекта локально
Клонировать репозиторий и перейти в него:
```
git clone https://github.com/wombatoff/dvmn_6
cd dvmn_6
```

Создать и активировать виртуальное окружение, обновить pip и установить зависимости:
```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Создать файл .env и заполнить его:
```
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=
VK_TOKEN=
REDIS_URL=
QUIZ_FILES_FOLDER=
```

Запустить бота:
```
python telegram_bot.py
python vk_bot.py
```


## Запуск проекта на сервере
### Подготовка сервера
- Запустить сервер и подключиться к нему:
```
ssh username@ip_address
```
- Установить обновления apt:
```
sudo apt upgrade -y
```
- Установить docker:
```
sudo apt-get install docker.io -y
```

- Клонировать репозиторий и перейти в него:
```
git clone https://github.com/wombatoff/dvmn_6
cd dvmn_6
```
- Создать файл .env и заполнить его:
```
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=
VK_TOKEN=
REDIS_URL=
QUIZ_FILES_FOLDER=
```
- Запустите docker-compose:
```
sudo docker-compose up -d
```

### Ссылки на рабочих ботов:
- [VK bot](https://vk.com/club220316320)

- [Telegram bot](https://t.me/wombtestbot)

### Автор:
[Wombatoff](https://github.com/wombatoff/)