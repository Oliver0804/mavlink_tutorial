#!/bin/bash

# 啟動 Docker Compose
echo "啟動 Docker Compose..."
docker-compose up -d

# 確保容器有足夠的時間啟動
echo "等待容器啟動..."
sleep 10


# 在新的終端窗口中啟動 MAVProxy 連接到 Rover
echo "在新的終端窗口中連接到 Rover..."
gnome-terminal -- bash -c "mavproxy.py --master=tcp:127.0.0.1:5761 \
 --out=udp:127.0.0.1:14551 \
 --map \
 --console; exec bash"
sleep 1

# 在另一個新的終端窗口中啟動 MAVProxy 連接到 Helicopter
echo "在新的終端窗口中連接到 Helicopter..."
gnome-terminal -- bash -c "mavproxy.py --master=tcp:127.0.0.1:5762 \
 --out=udp:127.0.0.1:14552 \
 --map \
 --console; exec bash"
sleep 1
echo "在新的終端窗口中連接到Rover 使用tcp:5761進行連線,轉發至14551..."

echo "在新的終端窗口中連接到Heli 使用tcp:5762進行連線,轉發至14552..."
