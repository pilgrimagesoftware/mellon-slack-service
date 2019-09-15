FROM python:3.7
LABEL maintainer="Paul Schifferer <paul@schifferers.net"

RUN apt-get -q update                    \
    && DEBIAN_FRONTEND=noninteractive    \
    && apt-get -q -y install python3-pip \
    && apt-get -q clean                  \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/flask-app/

COPY config/flask-app.ini /opt/flask-app
COPY mellon_core_service /opt/flask-app/
RUN ls -lR /opt/flask-app

WORKDIR /opt/flask-app
ENV HOME=/opt/flask-app
ENV FLASK_APP=mellon_slack_service:create_app
ENV FLASK_ENV="production"
ENV FLASK_DEBUG="False"
ENV DEBUG="False"
ENV CSRF_ENABLED="True"
ENV CSRF_SESSION_KEY="CSRF_SESSION_KEY_HERE"
ENV SECRET_KEY="SECRET_KEY_HERE"
ENV SLACK_APP_ID="SLACK_APP_ID_HERE"
ENV SENTRY_DSN="SENTRY_DSN_HERE"
ENV HOST="0.0.0.0"
ENV PORT="5000"

COPY requirements.txt /opt/flask-app
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD [ "flask", "run", "-h", "${HOST}", "-p", "${PORT}" ]
# CMD [ "waitress-serve", "--call", "mellon_slack_service:create_app" ]
