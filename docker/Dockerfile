FROM python:3.8
RUN pip install --upgrade pip
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD ./requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install uwsgi
