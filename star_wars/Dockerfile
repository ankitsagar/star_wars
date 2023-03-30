FROM python:3.10.10
COPY . /app/
WORKDIR /app
RUN groupadd -r sw && useradd -r -g sw sw
RUN apt-get update \
    && apt-get install -y \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x api-entrypoint.sh
