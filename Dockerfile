FROM python:3.11.9-alpine

# Set the working directory
WORKDIR /app
COPY . /app

CMD ["python", "download.py"]