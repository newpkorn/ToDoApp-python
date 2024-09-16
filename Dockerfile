FROM python:3.11-alpine

# Install only the necessary system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    build-base \
    sqlite-dev \
    curl-dev \
    zlib-dev \
    jpeg-dev

COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
EXPOSE 5000
CMD ["app.py"]