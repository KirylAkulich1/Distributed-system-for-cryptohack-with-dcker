FROM jpetazzo/dind

RUN apt update && apt install -y python && apt install -y python3-pip
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip3 install Flask uWSGI requests
RUN docker image pull python

WORKDIR /app
COPY app /app

EXPOSE 9090 9191

USER uwsgi

CMD ["uwsgi", "--http", "0.0.0.0:9090", "--wsgi-file", "/app/cryptohacker.py", \
"--callable", "app", "--stats", "0.0.0.0:9191"]

