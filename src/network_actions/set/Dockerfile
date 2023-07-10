FROM docker.uclv.cu/python:3.8

WORKDIR /dock_server

COPY ../requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# CMD ["python3", "main.py", "-i", "172.18.0.2", "-p", "8468", "-o", "set", "-k", "my-key", "-v", "my awesome value"]