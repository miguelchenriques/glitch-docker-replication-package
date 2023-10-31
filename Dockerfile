FROM debian:11

RUN apt-get update
RUN apt-get install -y ruby-full python3 python3-pip
RUN pip install puppetparser

COPY datasets/ datasets/
COPY . .

RUN pip install -r requirements.txt
RUN pip install -e GLITCH/
