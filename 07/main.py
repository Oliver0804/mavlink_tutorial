
# Description: This is a sample code for connecting to a drone and sending commands to it.
# docker build --tag ardupilot github.com/radarku/ardupilot-sitl-docker
## docker run -it --rm -p 5760:5760 ardupilot
## 或是於docker資料夾中運行docker-compose up

# 運行mavproxy
# mavproxy.py --master=tcp:127.0.0.1:5760 --out=udp:127.0.0.1:14550
## module console
## MAVProxy -> Show map and Show HUD
#setspeed N
#如果在自動飛行模式下，將車輛目標速度設置為Nm/s。

#takeoff ALTITUDE_IN_METERS
#向車輛發送自動起飛命令。它將認為起飛在 ALTITUDE_IN_METERSm（相對）完成。

#velocity X Y Z
#在局部東北向下 (x, y, z) 坐標系中設置所需的車輛速度。所有速度以 m/s 為單位。



import time
from pymavlink import mavutil

# 開始一個監聽UDP埠的連線
the_connection = mavutil.mavlink_connection('udpin:localhost:14550')

# 等待第一個心跳訊息

# 這會設定鏈路的遠端系統及元件的ID
the_connection.wait_heartbeat()

# 向飛機發送解鎖指令
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

# 等待指令確認訊息
print("等待指令確認訊息")
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

print("從系統接收到的心跳訊息 (系統 %u 元件 %u)" %
      (the_connection.target_system, the_connection.target_component))

# 向飛機發送改變模式的指令，設定模式為 "GUIDED"
#透過發送一個包含 MAV_CMD_DO_SET_MODE 指令的 COMMAND_LONG 消息來實現的​。
#https://ardupilot.org/dev/docs/mavlink-get-set-flightmode.html
#這裡是每個參數的詳細解釋：
#target_system: 無人機的系統ID。如果對象是飛行控制器，則此值可以是0。
#target_component: 無人機的組件ID。如果對象是飛行控制器，則此值可以是0。
#command: 設為 MAV_CMD_DO_SET_MODE，其值為176。
#confirmation: 一般設為0。
#param1: 設為 MAV_MODE_FLAG_CUSTOM_MODE_ENABLED，其值為1，表示啟用自定義模式。
#param2: 飛行模式的數字。您可以根據不同的無人機類型（例如飛機、直升機、潛水艇、輪式機器人、天線追蹤器等）選擇對應的飛行模式​2​。
    #對於飛機（Plane），GUIDED模式的數字為15
    #對於多旋翼機（Copter），GUIDED模式的數字為4
    #對於水下無人機（Sub），GUIDED模式的數字為4
    #對於地面車輛（Rover），GUIDED模式的數字為15
    #對於天線追蹤器（Tracker），並無GUIDED模式
    #https://github.com/ArduPilot/mavlink/blob/master/message_definitions/v1.0/ardupilotmega.xml
#param3 到 param7: 這些參數在這個指令中不被使用，所以都設為0。
print("改變模式為 'GUIDED'")
the_connection.mav.command_long_send(
    the_connection.target_system,
    the_connection.target_component,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    0,    # confirmation 
    1,    # MAV_MODE_FLAG_CUSTOM_MODE_ENABLED
    4,    # GUIDED mode for Copter
    0, 0, 0, 0, 0  # unused parameters
)
# 接收COMMAND_ACK訊息並輸出
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)




# 向飛機再次發送解鎖指令
print("解鎖")
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

time.sleep(1)
# 向飛機發送起飛指令，目標高度為40
print("起飛")
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 40)
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

print("從系統接收到的心跳訊息 (系統 %u 元件 %u)" %
      (the_connection.target_system, the_connection.target_component))

# 向飛機發送設定位置的指令
#the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,
#                        the_connection.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, int(0b110111111000), int(-35.3629849 * 10 ** 7), int(149.1649185 * 10 ** 7), 10, 0, 0, 0, 0, 0, 0, 1.57, 0.5))

while True:
    # 接收SERVO_OUTPUT_RAW訊息，並印出PWM輸出值
    msg = the_connection.recv_match(type='SERVO_OUTPUT_RAW', blocking=True)
    if msg:
        print("PWM輸出：", msg.servo1_raw, msg.servo2_raw, msg.servo3_raw, msg.servo4_raw, msg.servo5_raw, msg.servo6_raw, msg.servo7_raw, msg.servo8_raw)

    # 接收GLOBAL_POSITION_INT訊息，並印出目前的高度
    msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    if msg:
        print("目前的高度： %s" % msg.relative_alt)

    # 接收LOCAL_POSITION_NED訊息，並印出飛機的位置訊息
    msg = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True)
    if msg:
        print("飛機的位置訊息：", msg)

    # 接收RAW_IMU訊息，並印出IMU訊息
    msg = the_connection.recv_match(type='RAW_IMU', blocking=True)
    if msg:
        print("IMU訊息：", msg)

