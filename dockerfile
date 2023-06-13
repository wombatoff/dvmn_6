FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "telegram_bot.py", "&", "python", "vk_bot.py"]