# Ubuntu 20.04ベースイメージを使用
FROM ubuntu:20.04

# DEBIAN_FRONTENDを非対話モードに設定
ENV DEBIAN_FRONTEND=noninteractive

# パッケージのアップデートとアップグレード
RUN apt-get update && apt-get upgrade -y

# 必要なパッケージのインストール
RUN apt-get install -y python3.9 python3.9-dev python3.9-distutils curl
# RUN apt-get install -y python3.9 python3.9-dev python3-pip python3.9-distutils curl

# Python 3.9をデフォルトに設定
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

# pipのアップグレードと必要なPythonパッケージのインストール
RUN pip install --upgrade pip
# RUN python3.9 -m pip install --upgrade pip
# RUN python3.9 -m pip install django==3.1

# イメージのディレクトリを変更
WORKDIR /code

# # GDAL 3.2.2のインストールの前に
# # software-properties-commonとpython3-aptをインストール
# RUN apt-get update && apt-get install -y software-properties-common python3-apt

# GDAL 3.2.2のインストール
# RUN apt-get install -y software-properties-common
# RUN add-apt-repository ppa:ubuntugis/ppa
# RUN apt-get update

RUN apt-get install -y gdal-bin libgdal-dev python3-gdal

# # GDALライブラリのインストール
# RUN apt-get install -y libgdal-dev
# RUN echo ${gdal-config --version}
# RUN python3.9 -m pip install GDAL==$(gdal-config --version)

# postgis関連
RUN apt-get install -y binutils libproj-dev gdal-bin
RUN apt-get install -y python3-psycopg2 python3-psycopg2-dbg postgresql-client

COPY requirements.txt /code/
RUN pip install -r requirements.txt

# ダウングレードするならここから
# RUN pip install numpy
# RUN pip install uwsgi
# RUN pip install GDAL
# RUN pip install django==3.1
RUN pip install setuptools==57.4.0

# RUN apt-get install -y postgresql-client
COPY ./Pipfile /code/Pipfile
# RUN pipenv install --system --skip-lock

# # 使用するベースイメージを指定
# FROM ubuntu:20.04

# # 環境変数を設定
# ENV DEBIAN_FRONTEND=noninteractive
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # インストールするパッケージとPython 3.9をインストール
# RUN apt-get update -y && apt-get install -y \
#     curl \
#     locales\
#     python3.9 \
#     python3-pip 
#     # && apt-get clean 

# RUN apt-get update -y && apt-get install -y \
#     python3-gdal \
#     gdal-bin \
#     gdal-data \
#     python3-dev \
#     binutils \
#     build-essential \
#     libproj-dev \
#     libgdal-dev 
#     # && apt-get clean 


# # Python 3.9をデフォルトのPythonとして設定
# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
# # pipをアップグレード
# RUN python3 -m pip install --upgrade pip

# # RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py #python3.7以上
# # RUN curl https://bootstrap.pypa.io/pip/3.6/get-pip.py -o get-pip.py
# # RUN python3 get-pip.py
# # RUN pip install --upgrade pip
# RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 

# ENV LANG en_US.utf8
# RUN mkdir /code
# WORKDIR /code
# RUN pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"
# RUN pip install cffi

# # RUN pip install pipenv
# RUN pip install setuptools
# RUN pip install numpy
# # RUN pip install uwsgi
# RUN pip install Django==3.1
# # RUN pip install GDAL
# # ==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"


# # # RUN pip install wheel
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# # RUN pip install uwsgi 
# # RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
# # RUN export C_INCLUDE_PATH=/usr/include/gdal
# # RUN export CPLUS_INCLUDE_PATH=/usr/bin/gdal
# # RUN export C_INCLUDE_PATH=/usr/bin/gdal

# RUN apt-get install -y postgresql-client
# COPY ./Pipfile /code/Pipfile
# RUN pipenv install --system --skip-lock
# # COPY . /code/