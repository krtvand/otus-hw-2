FROM python:3.8-slim

#RUN apk update && \
#    apk add --virtual build-deps gcc python-dev musl-dev && \
#    apk add postgresql-dev && \

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /code
ADD . /code/
RUN pip install .

CMD ["hello_app"]

EXPOSE 8000