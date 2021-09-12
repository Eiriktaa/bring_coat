FROM python:3.9-slim-buster
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY weather.py .
CMD ["python3","weather.py"]
