FROM python:latest

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["flask", "--app", "hello.py", "run", "--host=0.0.0.0"]
