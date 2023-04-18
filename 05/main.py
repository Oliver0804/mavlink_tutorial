import time
from pymavlink import mavutil

def arm_and_takeoff(connection, target_altitude):
    print("起飛中...")

    # 首先將無人機切換到指定模式，例如GUIDED模式
    connection.mav.set_mode_send(
        connection.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mavutil.mavlink.COPTER_MODE_GUIDED
    )

    # 上鎖並啟動無人機
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1, 0, 0, 0, 0, 0, 0
    )

    # 設定目標高度
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0, 0, 0, 0, 0, 0,
        target_altitude
    )

def hover_and_land(connection, hover_time, land_time):
    print("懸停 {} 秒...".format(hover_time))
    time.sleep(hover_time)

    print("降落中...")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND,
        0,
        0, 0, 0, 0, 0, 0, 0
    )

    print("等待 {} 秒後斷開連接".format(land_time))
    time.sleep(land_time)
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        0, 0, 0, 0, 0, 0, 0
    )
    print("無人機已降落並解除電機上鎖")


def main():
    connection = mavutil.mavlink_connection("udp:127.0.0.1:14550")
    print("等待飛行器連接...")
    connection.wait_heartbeat()
    print("飛行器已連接")

    target_altitude = 10  # 目標高度，單位：米
    arm_and_takeoff(connection, target_altitude)

    hover_time = 30  # 懸停時間，單位：秒
    land_time = 30   # 降落時間，單位：秒
    hover_and_land(connection, hover_time, land_time)

if __name__ == "__main__":
    main()
