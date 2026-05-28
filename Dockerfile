FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# copy requirements
COPY requirements.txt .

# install python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy source
COPY . .

# flask port
EXPOSE 5000

# run flask app
CMD ["python", "app.py"]
