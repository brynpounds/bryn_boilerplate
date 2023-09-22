FROM python:3.11.5

WORKDIR /app
COPY ./app /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install openssl

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "-w", "1", "--threads", "12"]
