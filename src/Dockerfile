FROM docker.uclv.cu/python:3.8

WORKDIR /dock_server

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "cli/cli.py"]