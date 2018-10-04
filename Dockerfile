FROM python:2.7-alpine

COPY . /app

RUN pip install crontabs

WORKDIR /app

VOLUME [ "/app/conf" ]

CMD [ "python", "main.py" ]
