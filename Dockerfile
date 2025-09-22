FROM alpine:3.20

RUN apk add --no-cache python3 py3-pip && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "servidor.py"]