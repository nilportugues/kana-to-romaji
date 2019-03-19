sudo apt-get install -y python3 \
						python-dev \
						python3-dev \
						build-essential \
						libssl-dev \
						libffi-dev \
						libxml2-dev \
						libxslt1-dev \
						zlib1g-dev \
						python-pip

sudo apt-get install -y mecab mecab-ipadic-utf8 libmecab-dev swig

sudo apt-get install -y python3-setuptools \
					mecab \
					mecab-python3 \
					mecab-naist-jdic \
					libmecab-dev \
					python3-pip

pip3 install mecab
pip3 install mecab-python3
pip3 install pykakasi

pip3 install Flask
pip3 install flask-restplus
pip3 install flask-restful-swagger-2
pip3 install urllib3==1.22
