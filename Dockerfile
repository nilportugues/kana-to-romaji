
FROM python:3.7.2

RUN apt-get update

RUN apt-get -y install nginx
RUN useradd -s /bin/false nginx
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf

RUN apt-get -y install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip

RUN apt install -y mecab mecab-ipadic-utf8 libmecab-dev swig

RUN apt install -y 	python3-setuptools \
					mecab \
					mecab-naist-jdic \
					libmecab-dev \
					python3-pip


RUN pip3 install mecab-python3
RUN pip3 install pykakasi
RUN pip3 install Flask
RUN pip3 install flask-restplus
RUN pip3 install flask-restful-swagger-2
RUN pip3 install urllib3==1.22


COPY ./api /app
WORKDIR /app
RUN cd /app && \
    python3 setup.py install && \
    pip3 install uwsgi

## Copy files for uwsgi
RUN mkdir -p /opt/uwsgi/
COPY ./docker/uwsgi/uwsgi.ini /opt/uwsgi/uwsgi.ini

## Copy files for nginx
COPY ./docker/nginx/conf/app.conf /etc/nginx/sites-enabled/app.conf

# Exposed ports
EXPOSE 80

## Copy over the entrypoint
COPY ./docker/entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]