FROM docker.uclv.cu/python:3.8

WORKDIR /dock_server

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "main.py"]