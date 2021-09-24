FROM python:slim

RUN useradd dostuffuser

WORKDIR /home/DoStuff

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY dostuff.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP dostuff.py

RUN chown -R dostuffuser:dostuffuser ./
USER dostuffuser

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]