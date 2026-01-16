FROM python:latest

RUN pip install uv

RUN apt-get update && \
    apt-get install -y fish && \
    chsh -s /bin/fish