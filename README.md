
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
REDIS_PASSWORD=
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
REDIS_PASSWORD=
```
- Разверните Docker-контейнер:
```
docker build -t dvmn_6 .
```
```
sudo docker run -d \
  --name dvmn_6 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env \
  --env-file .env \
  --restart unless-stopped \
  dvmn_6 \
  python telegram_bot.py \
  python vk_bot.py
```

### Автор:

[Wombatoff](https://github.com/wombatoff/)