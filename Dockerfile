FROM python:3
ENV PYTHONUNBUFFERED=1


#ENV LANG es_PE.UTF-8
#ENV LC_ALL es_PE.UTF-8

RUN mkdir /code
WORKDIR /code

COPY ["requirements.txt", "/code/"]
RUN pip install -r requirements.txt

COPY [".", "/code/"]