# Pagure
# Build using: sudo docker build -t "ircb:0.0.1" --rm=true --no-cache .
#
# NAME         pagure
# VERSION      0.0.1
# LAST_UPDATED 2017-03-06 14:47

FROM fedora/redis:latest
MAINTAINER Farhaan Bukhsh <farhaan.bukhsh@gmail.com>

RUN dnf -y update && dnf clean all
RUN dnf install -y make automake gcc gcc-c++ kernel-devel libffi libffi-devel \
                   zeromq zeromq-devel redhat-rpm-config
RUN dnf install -y python2-devel python-setuptools python-nose py-bcrypt python-alembic \
                   python-pip python3-devel openssl-devel redis python3-pip

RUN pip3.4 install Flask==0.10.1 Flask-SQLAlchemy==2.0 Flask-User==0.6.11 \
                   SQLAlchemy==1.0.13 SQLAlchemy-Utils==0.30.15 irc3==0.9.3 \
                   alembic==0.8.3 WTForms-Alchemy==0.15.0 click==6.3 \
                   aioredis==0.2.4 tabulate==0.7.5 aiohttp==1.2.0 \
                   aiohttp-auth==0.1.1 aiohttp-session[secure]==0.5.0 \
                   aiozmq==0.7.1 msgpack-python==0.4.7 PyYAML==3.11 redis

EXPOSE 9000 10000 6379

CMD ["redis-service"]

