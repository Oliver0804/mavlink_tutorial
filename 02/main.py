# 引入相關模組
import time
from pymavlink import mavutil

# 創建MAVLink連接，這裡以串口連接為例
# 如果是模擬器，可以使用 "udp:127.0.0.1:14550" 進行連接
connection = mavutil.mavlink_connection("/dev/ttyACM1", baud=115200)
#connection = mavutil.mavlink_connection("udp:127.0.0.1:14550")

# 等待接收到無人機的heartbeat訊息
print("等待無人機連接...")
while True:
    msg = connection.recv_match(type='HEARTBEAT', blocking=True)
    if msg:
        print("無人機已連接")
        break



