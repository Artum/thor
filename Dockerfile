FROM python:3.9-slim-buster
RUN mkdir /thor 
COPY . /thor
WORKDIR /thor

EXPOSE 5000

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
ENV WSGI_HOST="0.0.0.0"
ENV WSGI_PORT="5000"

ENV FLASK_SECRET_KEY="74b40eef603f5a5cd2eca4f8c4e60e25"
ENV FLASK_ENV="development"
ENV FLASK_DEBUG=1

ENV JWT_SECRET_KEY="549adff7746a1c73825b103f2c2160fc"

ENV MYSQL_HOST="127.0.0.1"
ENV MYSQL_PORT="3369"
ENV MYSQL_USER="user"
ENV MYSQL_PASSWORD="bbc2cd54d94b680fb961a0772abdf977"
ENV MYSQL_DB="thor"

ENV GOOGLE_CLIENT_ID=""
ENV GOOGLE_CLIENT_SECRET=""

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["python", "wsgi.py"]