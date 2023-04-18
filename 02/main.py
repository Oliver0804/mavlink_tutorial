# 引入相關模組
import time
from pymavlink import mavutil

# 創建MAVLink連接，這裡以串口連接為例
# 如果是模擬器，可以使用 "udp:127.0.0.1:14550" 進行連接
connection = mavutil.mavlink_connection("serial:/dev/ttyUSB0", baud=57600)

# 等待接收到無人機的heartbeat訊息
print("等待無人機連接...")
while True:
    msg = connection.recv_match(type='HEARTBEAT', blocking=True)
    if msg:
        print("無人機已連接")
        break

# 持續讀取無人機狀態資訊
while True:
    # 接收MAVLink訊息
    msg = connection.recv_match(blocking=True)

    # 判斷訊息類型並處理
    if msg.get_type() == "GLOBAL_POSITION_INT":
        # 解析經緯度和高度資訊
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt = msg.alt / 1e3
        print("經度：{:.6f}，緯度：{:.6f}，高度：{:.2f}米".format(lon, lat, alt))
    elif msg.get_type() == "ATTITUDE":
        # 解析機態角資訊
        roll = msg.roll
        pitch = msg.pitch
        yaw = msg.yaw
        print("機態角 - Roll：{:.2f}，Pitch：{:.2f}，Yaw：{:.2f}".format(roll, pitch, yaw))

    # 避免過度佔用CPU資源
    time.sleep(0.1)

