FROM terrillo/python3flask:latest

RUN apt-get update
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


# STATIC paths for file.
# Don't use flask static. Nginx is your friend
ENV STATIC_URL /static
ENV STATIC_PATH /app/static

# Place your flask application on the server
COPY ./api /app
WORKDIR /app


# NGINX setup
COPY ./nginx.sh /nginx.sh
RUN chmod +x /nginx.sh

ENV PYTHONPATH=/app

ENTRYPOINT ["/nginx.sh"]

# Start Server
CMD ["/start.sh"]

EXPOSE 80 443