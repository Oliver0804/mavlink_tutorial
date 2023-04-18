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
def set_waypoints(connection, waypoints):
    print("設定導航點...")
    for i, waypoint in enumerate(waypoints):
        lat, lon, alt = waypoint
        connection.mav.mission_item_send(
            connection.target_system,
            connection.target_component,
            i,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0, 0, 0, 0, 0, 0,
            lat, lon, alt
        )
        print(f"導航點 {i + 1} 已設定：緯度 {lat}, 經度 {lon}, 高度 {alt}")

def start_mission(connection):
    print("開始執行導航任務...")
    connection.mav.set_mode_send(
        connection.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mavutil.mavlink.COPTER_MODE_AUTO
    )

def rtl(connection):
    print("返回起點...")
    connection.mav.set_mode_send(
        connection.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mavutil.mavlink.COPTER_MODE_RTL
    )

def main():
    connection = mavutil.mavlink_connection("udp:127.0.0.1:14550")
    print("等待飛行器連接...")
    connection.wait_heartbeat()
    print("飛行器已連接")

    target_altitude = 10
    arm_and_takeoff(connection, target_altitude)

    waypoints = [
        (23.123456, 121.234567, target_altitude),
        (23.234567, 121.345678, target_altitude),
        (23.345678, 121.456789, target_altitude)
    ]
    set_waypoints(connection, waypoints)

    start_mission(connection)

    # 在此處插入等待任務完成的程式碼，例如：
    # - 通過監聽任務進度訊息來判斷任務完成
    # - 或者設定一個固定的等待時間
    print("等待導航任務完成...")
    time.sleep(60)

    rtl(connection)
    print("等待飛行器返回起點...")
    time.sleep(30)

    connection.mav.command_long_send(
    connection.target_system,
    connection.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    0, 0, 0, 0, 0, 0, 0
    )
    print("無人機已降落並解除電機上鎖")

if __name__ == "__main__":
    main()