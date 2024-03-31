FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update -y && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

COPY . .

CMD ["sh", "-c", "python manage.py migrate  && python manage.py collectstatic --no-input && gunicorn scrolls.wsgi:application -b 0.0.0.0:8001"]
