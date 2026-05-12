# เปลี่ยนจาก slim ธรรมดา เป็น bullseye-slim เพื่อให้ Docker รู้ว่าเป็นตัวใหม่
FROM --platform=linux/amd64 python:3.9-bullseye

WORKDIR /app

# ลงตัวต่อ MySQL (Bullseye จะเสถียรกว่าบน Windows)
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]