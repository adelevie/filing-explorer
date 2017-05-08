FROM python:3

ENV PYTHONUNBUFFERED 1

ENV workdir /app
RUN mkdir -p $workdir
WORKDIR $workdir

ADD requirements.txt $workdir/requirements.txt

RUN pip install --target /usr/local/lib/python3.6/site-packages/simhash_py git+https://github.com/seomoz/simhash-py.git
RUN pip install -r requirements.txt
