FROM python:3.9

MAINTAINER Dmitry Abakumov <killerinshadow2@gmail.com>

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bot.py .
COPY .env .

ENTRYPOINT ["python", "bot.py"]
