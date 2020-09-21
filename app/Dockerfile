FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y libssl-dev ruby-dev rubygems cron rsyslog

RUN pip install setuptools scrypt wheel pytest hivepy

RUN gem install sass

RUN sed -i '/imklog/s/^/#/' /etc/rsyslog.conf

WORKDIR /app

RUN groupadd -r django && useradd -m -r -g django django

RUN mkdir /data \
    && chown django.django /data

RUN mkdir /data/static \
    && chown django.django /data/static

RUN mkdir /data/media \
    && chown django.django /data/media

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY . /app
RUN chown -R django /app

COPY compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY compose/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh \
    && chmod +x /start.sh \
    && chown django /start.sh

COPY compose/django/configure_and_run_cron.sh /configure_and_run_cron.sh
RUN chmod +x /configure_and_run_cron.sh \
    && chown django /configure_and_run_cron.sh

COPY compose/django/cron.sh /cron.sh
RUN chmod +x /cron.sh \
    && chown django /cron.sh

ENTRYPOINT ["/entrypoint.sh"]
