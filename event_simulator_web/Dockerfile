FROM python:3.7.7

RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin gettext

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
