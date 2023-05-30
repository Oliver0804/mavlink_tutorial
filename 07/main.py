
# Description: This is a sample code for connecting to a drone and sending commands to it.
# docker build --tag ardupilot github.com/radarku/ardupilot-sitl-docker
# docker run -it --rm -p 5760:5760 ardupilot

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

# 向飛機再次發送解鎖指令
print("解鎖")
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

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

while 0:
    msg = the_connection.recv_match(type='SERVO_OUTPUT_RAW', blocking=True)
    print("PWM Outputs: ", msg.servo1_raw, msg.servo2_raw, msg.servo3_raw, msg.servo4_raw, msg.servo5_raw, msg.servo6_raw, msg.servo7_raw, msg.servo8_raw)



# 秀出高度
while True:
    msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    if msg:
        print("Current altitude: %s" % msg.relative_alt)


# 持續接收飛機的位置訊息
while True:
    msg = the_connection.recv_match(
        type='LOCAL_POSITION_NED', blocking=True)
    print(msg)

# IMU
while True:
    msg = the_connection.recv_match(
        type='RAW_IMU', blocking=True)
    print(msg)
