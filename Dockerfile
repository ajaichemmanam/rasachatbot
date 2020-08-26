# FROM ubuntu:18.04
# ENTRYPOINT []
# RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa
# ADD . /app/
# RUN chmod +x /app/start_services.sh
# CMD /app/start_services.sh

FROM rasa/rasa:1.10.11

USER root
ADD ./models /app/models/
ADD ./config /app/config/
ADD ./actions /app/actions/
ADD ./scripts /app/scripts/
ADD ./trackerStore /app/trackerStore/
ADD ./data /app/data/
ADD ./domain.yml /app/
ADD ./config.yml /app/

RUN chmod +x /app/scripts/*
ENTRYPOINT []
CMD /app/scripts/start_services.sh