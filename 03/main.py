import time
from pymavlink import mavutil

def request_system_status(connection):
    # 向飛行器發送請求，詢問系統狀態
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        0,
        mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS,
        0, 0, 0, 0, 0, 0)

# 創建與飛行器的MAVLink連接，這裡以串口連接為例
# 如果是模擬器，可以使用 "udp:127.0.0.1:14550" 進行連接
connection = mavutil.mavlink_connection("/dev/ttyACM1", baud=57600)

# 等待接收到飛行器的心跳訊息
print("等待飛行器連接...")
while True:
    msg = connection.recv_match(type='HEARTBEAT', blocking=True)
    if msg:
        print("飛行器已連接")
        break




# 持續讀取飛行器狀態訊息
while True:
    # 發送請求，詢問飛行器的系統狀態
    request_system_status(connection)
    
    # 接收MAVLink訊息
    msg = connection.recv_match(blocking=True)

    # 判斷訊息類型並處理
    if msg.get_type() == "SYS_STATUS":
        # 解析電池電壓和電流
        voltage = msg.voltage_battery / 1000.0
        current = msg.current_battery / 100.0
        print("電池電壓：{:.2f}伏特，電流：{:.2f}安培".format(voltage, current))

        # 解析CPU負載
        load = msg.load / 10.0
        print("CPU負載：{:.1f}%".format(load))

        # 解析通訊丟包率
        drop_rate = msg.drop_rate_comm / 100.0
        print("通訊丟包率：{:.2f}%".format(drop_rate))

        # 避免過度佔用CPU資源
        time.sleep(1)
