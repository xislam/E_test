FROM python:3.11
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
RUN mkdir /code
WORKDIR /code
COPY req.txt /code/
RUN pip install --upgrade pip
RUN pip install -r req.txt
ADD . /code/
