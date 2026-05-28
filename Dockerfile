# Sử dụng phiên bản Python hiện đại và ổn định
FROM python:3.12-slim

# Thiết lập biến môi trường để không tạo ra các file .pyc (tiết kiệm không gian)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cài đặt các thư viện hệ thống cần thiết cho Pygame và kết nối Database
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Nâng cấp pip lên bản mới nhất trước khi cài đặt dependencies
RUN pip install --no-cache-dir --upgrade pip

# Copy và cài đặt requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code vào sau cùng để tận dụng cache
COPY . .

# Chạy file chính
CMD ["python", "NNFS.py"]
