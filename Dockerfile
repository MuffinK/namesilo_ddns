FROM python:2.7-alpine

ADD . /app

RUN pip install crontabs

WORKDIR /app

VOLUME [ "/app/ddns.conf" ]

CMD [ "python", "main.py" ]
