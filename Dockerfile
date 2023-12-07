###############
# Build Stage #
###############

FROM python:3.10-slim as build

RUN apt update && apt install -y default-libmysqlclient-dev curl gcc python3-dev libc-dev libffi-dev

WORKDIR /opt/venv

RUN python3 -m venv /opt/venv

COPY requirements.txt /opt/venv/

ENV PATH="/opt/venv/bin:$PATH" VIRTUAL_ENV="/opt/venv"

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt


#####################
# Production Stage #
#####################

FROM python:3.10-slim

WORKDIR /opt/venv

COPY --from=build /opt/venv /opt/venv

RUN apt update && apt install -y default-libmysqlclient-dev curl

ENV PATH="/opt/venv/bin:$PATH" VIRTUAL_ENV="/opt/venv"

WORKDIR /app

COPY . .

ENTRYPOINT ["/opt/venv/bin/gunicorn"]
CMD ["-c", "gunicorn.conf.py"]
