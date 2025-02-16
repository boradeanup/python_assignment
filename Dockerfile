FROM python:3.9.6-slim-buster

# Set up a working directory
WORKDIR /app
COPY requirements.txt /app/

RUN apt-get -y update && \
    apt-get -y install libpq-dev python-dev gcc musl-dev


# Install dependencies
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org pipenv gunicorn
RUN pip install -r requirements.txt

# copy files
COPY * /app/
RUN mkdir financial
COPY financial/* financial/

RUN cd financial/

CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]
# CMD /bin/bash start