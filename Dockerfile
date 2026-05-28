FROM python:3.8-slim

# Cài đặt thư viện hệ thống cần thiết cho Pygame và MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libmariadb-dev-compat \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Chạy file chính (thường là main.py hoặc tương đương)
CMD ["python", "main.py"]