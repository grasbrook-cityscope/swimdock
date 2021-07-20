FROM python:3.8

# Install dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y unzip wget git build-essential -y
RUN pip install pyswmm

COPY ./app /app
COPY ./data /data

WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "-u", "main.py" ]
CMD [] 
