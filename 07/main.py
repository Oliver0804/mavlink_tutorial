#引入pymavlink庫，並且引入mavutil
#這個程式碼主要是用來控制飛機的起飛、降落、相對移動
#首先我們要先建立一個連接，這個連接是用來跟飛機通訊的
#我們可以透過mavutil.mavlink_connection來建立連接
#這個函數需要一個參數，就是我們要連接的飛機的位址
#這裡我們使用
import time
from pymavlink import mavutil

#arm_and_takeoff函數需要一個連接和一個參數，這個參數是用來設定飛機的起飛高度
def arm_and_takeoff(aTargetAltitude):
    print("準備起飛！")
    while not vehicle.is_armable:
        print("等待飛行器初始化...")
        time.sleep(1)

    # 這裡我們先設定飛機的模式為GUIDED模式
    vehicle.mode = VehicleMode("GUIDED")

    # 等待模式設定完成
    while vehicle.mode != "GUIDED":
        print("等待模式設定完成...")
        time.sleep(1)

    # 解除武裝
    vehicle.armed = True

    # 等待解除武裝完成
    while not vehicle.armed:
        print("等待解除武裝完成...")
        time.sleep(1)

    print("起飛！")
    vehicle.simple_takeoff(aTargetAltitude)

    # 當飛機的高度大於目標高度的95%時，就跳出迴圈
    while True:
        print("目前高度：", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("已達到目標高度")
            break
        time.sleep(1)    

#RTL函數需要一個連接，然後就是讓飛機回到起飛點
def RTL(connection):
    print("返航！")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
        0,
        0, 0, 0, 0, 0, 0, 0
    )

#land函數需要一個連接，然後就是讓飛機降落
def land(connection):
    print("降落！")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND,
        0,
        0, 0, 0, 0, 0, 0, 0
    )

def change_mode_circle(connection):
    print("繞圈！")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LOITER_UNLIM,
        0,
        0, 0, 0, 0, 0, 0, 0
    )

#change mode to GUIDED
def change_mode_guided(connection):
    print("change mode to GUIDED")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,
        0, 0, 0, 0, 0, 0, 0
    )

#change mode to AUTO
def change_mode_auto(connection):
    print("change mode to AUTO")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,
        1, 0, 0, 0, 0, 0, 0
    )
#輸入前後左右距離與高度 對應發送mavlink指令
def move_relative(connection, distance_x, distance_y, distance_z):
    print("移動相對距離")
    connection.mav.set_position_target_local_ned_send(
        0,
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0, 0, 0,
        distance_x, distance_y, distance_z,
        0, 0, 0,
        0, 0
    )




#主程序入口
#這裡我們先建立一個連接，然後呼叫arm_and_takeoff函數，起飛高度是10公尺
#起飛之後，我們再呼叫move_relative函數，讓飛機向前移動10公尺，然後等待5秒
#接著我們再呼叫move_relative函數，讓飛機向後移動10公尺，然後等待5秒
#最後我們呼叫disarm函數，讓飛機降落並且解除武裝

if __name__ == "__main__":
    connection = mavutil.mavlink_connection("udp:127.0.0.1:14550")
    arm_and_takeoff(10)
    # 使用方向鍵控制飛機移動
    while True:
        try:
            input_char = input("請輸入指令：")
            if input_char == "w":
                print("前進")
                move_relative(connection, 10, 0, 0)
            elif input_char == "s":
                print("後退")
                move_relative(connection, -10, 0, 0)
            elif input_char == "a":
                print("左移")
                move_relative(connection, 0, -10, 0)
            elif input_char == "d":
                print("右移")
                move_relative(connection, 0, 10, 0)
            elif input_char == "q":
                print("返航")
                RTL(connection)
            elif input_char == "e":
                print("降落")
                land(connection)
            elif input_char == "r":
                print("繞圈")
                circle(connection)
            elif input_char == "z":
                print("change mode to GUIDED")
                change_mode_guided(connection)
            elif input_char == "x":
                print("change mode to AUTO")
                change_mode_auto(connection)
            elif input_char == "c":
                print("change mode to RTL")
                RTL(connection)
            else:
                print("無效指令")
        except KeyboardInterrupt:
            print("程式結束")
            break