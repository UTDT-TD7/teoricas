FROM python:3

# Clone and build eventsim
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /usr/src/app
COPY etl.py ./
COPY ge.py ./

#CMD [ "python", "-u", "./etl.py" ]
