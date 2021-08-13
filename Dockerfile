FROM python:3.8-slim-buster

WORKDIR /project

# ARG AWS_ACCESS_KEY_ID
# ARG AWS_SECRET_ACCESS_KEY
# ARG AWS_DEFAULT_REGION
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get update \
    && apt-get install -y \
    git \
    libzbar0 \
    && apt-get clean

COPY ./requirements.txt ./
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . .

WORKDIR /usr/src/app
RUN cp -r /project/* /usr/src/app && rm -rf /project

CMD ["flask", "run"]