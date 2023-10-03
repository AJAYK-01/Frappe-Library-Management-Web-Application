FROM python:3.10.8-alpine

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["flask db upgrade", "&&",  "flask run"]