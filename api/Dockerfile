FROM alpine:3.17

RUN apk update
RUN apk upgrade
# libpq-dev[DB_DEPEND] TODO
RUN apk add python3 python3-dev libpq-dev gcc musl-dev postgresql-dev libffi-dev

# Installing all dependencies
RUN python3 -m ensurepip
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
