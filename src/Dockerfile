FROM docker.uclv.cu/python:3.8

WORKDIR /test_docker

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]