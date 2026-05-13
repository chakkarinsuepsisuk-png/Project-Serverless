# ใช้ bullseye-slim เพื่อลดขนาดจาก ~200MB เหลือเพียง ~40-50MB ใน Layer ฐาน
FROM --platform=linux/amd64 python:3.9-slim-bullseye

WORKDIR /app

# ติดตั้ง Dependencies สำหรับ MySQL Client 
# การใช้ slim จำเป็นต้องลงเครื่องมือ build ชั่วคราวเพื่อให้ติดตั้ง mysqlclient ผ่าน pip ได้
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# ติดตั้ง library โดยไม่เก็บ cache เพื่อประหยัดพื้นที่
RUN pip install --no-cache-dir -r requirements.txt

COPY . .





CMD ["python", "app.py"]