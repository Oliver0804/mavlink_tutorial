import time
from pymavlink import mavutil

# 建立與無人機的MAVLink連接，這裡以連接到模擬器為例
# 如果是實際無人機，可以使用 "serial:/dev/ttyUSB0", baud=57600 進行連接
connection = mavutil.mavlink_connection("udp:127.0.0.1:14550")

# 等待接收到飛行器的心跳訊息
print("等待飛行器連接...")
while True:
    msg = connection.recv_match(type='HEARTBEAT', blocking=True)
    if msg:
        print("飛行器已連接")
        break

# 向飛行器請求IMU和GPS數據
connection.mav.request_data_stream_send(
    connection.target_system,
    connection.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_EXTENDED_STATUS,
    10,  # 請求數據流的頻率，10Hz
    1    # 啟用數據流
)

# 持續讀取飛行器GPS和IMU資訊
while True:
    # 接收MAVLink訊息
    msg = connection.recv_match(blocking=True)

    # 判斷訊息類型並處理
    if msg.get_type() == "SCALED_IMU":
        print("加速度計：x={}, y={}, z={}".format(msg.xacc, msg.yacc, msg.zacc))
        print("陀螺儀：x={}, y={}, z={}".format(msg.xgyro, msg.ygyro, msg.zgyro))
        print("磁力計：x={}, y={}, z={}".format(msg.xmag, msg.ymag, msg.zmag))

    elif msg.get_type() == "GPS_RAW_INT":
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt = msg.alt / 1e3
        print("GPS：緯度={}, 經度={}, 高度={}米".format(lat, lon, alt))
        print("GPS狀態：{}，可見衛星數：{}".format(msg.fix_type, msg.satellites_visible))

    # 避免過度佔用CPU資源
    time.sleep(0.1)
