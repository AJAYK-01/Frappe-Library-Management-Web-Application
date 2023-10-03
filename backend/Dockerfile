FROM python:3.10.8-alpine

# WORKDIR /app
WORKDIR /usr/src/app

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . /usr/src/app

RUN python -m pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["/bin/sh", "-c", "flask db upgrade && flask run"]

# CMD ["flask", "db" , "upgrade"]

# CMD ["flask", "run"]