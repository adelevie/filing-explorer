FROM python:3

# install node, then phantomjs
RUN apt-get update -qq && apt-get install -y build-essential nodejs npm nodejs-legacy
RUN npm install -g phantomjs-prebuilt

ENV PYTHONUNBUFFERED 1

ENV workdir /app
RUN mkdir -p $workdir
WORKDIR $workdir

ADD requirements.txt $workdir/requirements.txt

RUN pip install -r requirements.txt
