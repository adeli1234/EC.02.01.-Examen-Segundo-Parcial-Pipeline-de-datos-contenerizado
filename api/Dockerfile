FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    curl \
    && rm -rf /var/lib/apt-get/lists/*

WORKDIR /app

# Configurar SSH cliente para conectarse a hadoop
RUN mkdir -p /root/.ssh
COPY id_rsa /root/.ssh/id_rsa
COPY id_rsa.pub /root/.ssh/id_rsa.pub
RUN chmod 700 /root/.ssh && \
    chmod 600 /root/.ssh/id_rsa && \
    echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]