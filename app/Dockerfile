FROM ubuntu:20.04

ADD ../requirements.txt ./

RUN apt update \
&& apt install python3-pip -y \
&& pip install -r requirements.txt

ADD ./ /app/

WORKDIR /app/

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0
