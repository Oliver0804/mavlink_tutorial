#!/bin/bash

# 啟動 Docker Compose
echo "啟動 Docker Compose..."
docker-compose up -d

# 確保容器有足夠的時間啟動
echo "等待容器啟動..."
sleep 5


# 在新的終端窗口中啟動 MAVProxy 連接到 Rover
# 拓展輸出至 14551, 14561
echo "在新的終端窗口中連接到 Rover..."
gnome-terminal -- bash -c "mavproxy.py --master=tcp:127.0.0.1:5761 \
 --out=udp:127.0.0.1:14551 \
 --out=udp:127.0.0.1:14561 \
 --map \
 --console; exec bash"
sleep 1

# 在另一個新的終端窗口中啟動 MAVProxy 連接到 Helicopter
# 拓展輸出 14552, 14562
echo "在新的終端窗口中連接到 Helicopter..."
gnome-terminal -- bash -c "mavproxy.py --master=tcp:127.0.0.1:5762 \
 --out=udp:127.0.0.1:14552 \
 --out=udp:127.0.0.1:14562 \
 --map \
 --console; exec bash"


sleep 1
echo "在新的終端窗口中連接到Rover"
echo "Rover 使用tcp:5761進行連線,轉發至14551..."
echo "Rover 使用tcp:5761進行連線,轉發至14561..."

echo "在新的終端窗口中連接到Heli"
echo "Heli 使用tcp:5762進行連線,轉發至14552..."
echo "Heli 使用tcp:5762進行連線,轉發至14562..."