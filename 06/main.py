import time
from pymavlink import mavutil

def get_current_location(connection):
    msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    return msg.lat / 1E7, msg.lon / 1E7, msg.alt / 1E3  # returns lat, lon, alt

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

def move_relative(connection, x, y, z, wait_time):
    print(f"相對移動：x={x}, y={y}, z={z}")
    lat, lon, alt = get_current_location(connection)
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_REPOSITION,
        0,
        0, 0, 0, 0,
        lat + x,
        lon + y,
        alt + z
    )
    time.sleep(wait_time)

def main():
    connection = mavutil.mavlink_connection("udp:127.0.0.1:14550")
    print("等待飛行器連接...")
    connection.wait_heartbeat()
    print("飛行器已連接")

    target_altitude = 10
    arm_and_takeoff(connection, target_altitude)

    # 向左相對移動5公尺
    move_relative(connection, 0, -5, 0, 60)

    # 向右相對移動5公尺
    move_relative(connection, 0, 5, 0, 60)

    # 向前相對移動5公尺
    move_relative(connection, 5, 0, 0, 60)

    # 向後相對移動5公尺
    move_relative(connection, -5, 0, 0, 60)

    # 高度提高5公尺
    move_relative(connection, 0, 0, 5, 60)

    # 高度降低5公尺
    move_relative(connection, 0, 0, -5, 60)

    # 在此處添加降落和斷開無人機的代碼
    print("無人機操作完成")

if __name__ == "__main__":
    main()
