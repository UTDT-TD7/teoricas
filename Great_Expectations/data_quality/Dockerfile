FROM python:3

# Clone and build eventsim
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /usr/src/app
COPY ge.py ./

#CMD [ "python", "-u", "./ge.py" ]
