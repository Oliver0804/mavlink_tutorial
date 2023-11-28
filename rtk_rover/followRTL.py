from pymavlink import mavutil
import time
import math
import json
import socket
import pygame
import threading

from pymavlink.dialects.v20 import common as mavlink2

# 设置 RC 通道值
rc1 = 1500  # 示例值
rc2 = 1500  # 示例值
rc3 = 1500  # 示例值
rc4 = 1500  # 示例值

def get_current_location(connection):
    msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    return msg.lat / 1E7, msg.lon / 1E7, msg.alt / 1E3  # returns lat, lon, alt


def switch_to_rtl(vehicle):
    """
    Switch the given vehicle to RTL mode.

    :param vehicle: The vehicle to switch mode.
    """
    vehicle.set_mode(mavutil.mavlink.COPTER_MODE_RTL)
    print("Switched to RTL mode.")


def switch_to_loiter(vehicle):
    """
    Switch the given vehicle to Loiter mode.

    :param vehicle: The vehicle to switch mode.
    """
    vehicle.set_mode(mavutil.mavlink.COPTER_MODE_LOITER)
    print("Switched to Loiter mode.")


def switch_to_guided(vehicle):
    """
    Switch the given vehicle to Guided mode.

    :param vehicle: The vehicle to switch mode.
    """
    vehicle.set_mode(mavutil.mavlink.COPTER_MODE_GUIDED)
    print("Switched to Guided mode.")

def arm_throttle(vehicle):
    """
    Arms the vehicle and enables the throttle.

    :param vehicle: The vehicle to arm.
    """
    print("Arming motors")
    vehicle.mav.command_long_send(
        vehicle.target_system, 
        vehicle.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 
        0, 1, 0, 0, 0, 0, 0, 0  # Command to arm
    )
    #vehicle.motors_armed_wait()  # Wait until the motors are armed
    print("Motors armed")

def takeoff(vehicle, alt):
    """
    Commands the vehicle to take off and ascend to the specified altitude.

    :param vehicle: The vehicle to command.
    :param alt: The altitude to ascend to (in meters).
    """
    print(f"Taking off to {alt} meters")
    vehicle.mav.command_long_send(
        vehicle.target_system, 
        vehicle.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 
        0, 0, 0, 0, 0, 0, 0, alt  # Altitude to take off to
    )
    print(f"Vehicle is ascending to {alt} meters")


def get_current_yaw(vehicle):
    """
    获取飞行器的当前 YAW 角度。

    :param vehicle: 连接到飞行器的 MAVLink 连接实例。
    :return: YAW 角度（以弧度为单位）。
    """
    attitude = vehicle.recv_match(type='ATTITUDE', blocking=True)
    if attitude:
        print("Yaw:", attitude.yaw)
        return attitude.yaw
    else:
        return None


import math

def calculate_new_coordinates(lat, lon, yaw, distance):
    """
    根据给定的坐标、YAW 角度和距离计算新的坐标点，结果限制在小数点后七位。

    :param lat: 起始点纬度（以度为单位）。
    :param lon: 起始点经度（以度为单位）。
    :param yaw: YAW 角度（以弧度为单位）。
    :param distance: 距离（以米为单位）。
    :return: 新的坐标点（纬度、经度），小数点后七位。
    """
    # 将纬度和经度转换为弧度
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    R = 6371000  # 地球半径，单位：米
    delta = distance / R  # 角距离

    # 计算新的纬度和经度（以弧度为单位）
    new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(delta) + 
                            math.cos(lat_rad) * math.sin(delta) * math.cos(yaw))
    new_lon_rad = lon_rad + math.atan2(math.sin(yaw) * math.sin(delta) * math.cos(lat_rad),
                                       math.cos(delta) - math.sin(lat_rad) * math.sin(new_lat_rad))

    # 转换回角度并四舍五入到小数点后七位
    new_lat = round(math.degrees(new_lat_rad), 7)
    new_lon = round(math.degrees(new_lon_rad), 7)

    return new_lat, new_lon


def set_home_position(vehicle, lat, lon, alt):
    """
    设置无人机的 Home 位置。

    :param vehicle: 连接到无人机的 MAVLink 连接实例。
    :param lat: Home 位置的纬度。
    :param lon: Home 位置的经度。
    :param alt: Home 位置的高度（单位：米）。
    """
    # 使用 MAVLink 命令设置 Home 位置
    vehicle.mav.command_long_send(
        vehicle.target_system, vehicle.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_HOME,
        0,  # Confirmation
        0,  # Param 1: 0 to use specified lat/lon/alt
        0, 0, 0,  # Params 2-4 (unused)
        lat, lon, alt  # Params 5-7: Latitude, Longitude, Altitude
    )
    print(f"Setting new home position to{vehicle}: Latitude = {lat}, Longitude = {lon}, Altitude = {alt}")


def move_rc_channels_send(connection, SetRC1, SetRC2, SetRC3, SetRC4, wait_time):
    # 设置 RC 通道值
    rc1 = 1500  # 示例值
    rc2 = 1500  # 示例值
    rc3 = 1500  # 示例值
    rc4 = 1500  # 示例值
    msg = mavlink2.MAVLink_rc_channels_override_message(
        target_system=connection.target_system,
        target_component=connection.target_component,
        chan1_raw=SetRC1,
        chan2_raw=SetRC2,
        chan3_raw=SetRC3,
        chan4_raw=SetRC4,
        chan5_raw=0,
        chan6_raw=0,
        chan7_raw=0,
        chan8_raw=0
    )
    for x in range(0, wait_time):
        connection.mav.send(msg)
        print(".", end="")
        time.sleep(0.05)
    

def keyboard_listener():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Follow RTL")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print("姿態前傾")
                    move_rc_channels_send(heli, 1500, 1100, 1500, 1500, 2)

                elif event.key == pygame.K_s:
                    print("姿態往後")
                    move_rc_channels_send(heli, 1500, 1900, 1500, 1500, 2)

                elif event.key == pygame.K_a:
                    print("姿態向左")
                    move_rc_channels_send(heli, 1100, 1500, 1500, 1500, 2)

                elif event.key == pygame.K_d:
                    print("姿態向右")
                    move_rc_channels_send(heli, 1900, 1500, 1500, 1500, 2)
                elif event.key == pygame.K_q:
                    print("YAW向左")
                    move_rc_channels_send(heli, 1500, 1500, 1500, 1450, 1)
                elif event.key == pygame.K_e:
                    print("YAW向右")
                    move_rc_channels_send(heli, 1500, 1500, 1500, 1550, 1)
                elif event.key == pygame.K_k:
                    print("上升")
                    move_rc_channels_send(heli, 1500, 1500, 1900, 1500, 2)
                elif event.key == pygame.K_j:
                    print("下降")
                    move_rc_channels_send(heli, 1500, 1500, 1100, 1500, 2)
                elif event.key == pygame.K_r:
                    print("RTL")
                    switch_to_rtl(heli)
                elif event.key == pygame.K_l:
                    print("Loiter")
                    switch_to_loiter(heli)
                elif event.key == pygame.K_g:
                    print("Guided")
                    switch_to_guided(heli)
                elif event.key == pygame.K_u:#unlocked
                    print("arm throttle")
                    arm_throttle(heli)
                elif event.key == pygame.K_t:
                    print("takeoff")
                    takeoff(heli, 10)
                    
    pygame.quit()

# 创建并启动键盘监听线程
keyboard_thread = threading.Thread(target=keyboard_listener)
keyboard_thread.start()

#

# Establish a connection with the aircraft
#heli = mavutil.mavlink_connection('udp:127.0.0.1:14551')
# Establish a connection with the Rover ground station
#rover = mavutil.mavlink_connection('udp:127.0.0.1:14552')

def create_connection(conn_params):
    # 構造連接字符串並打印連接信息
    conn_string = construct_conn_string(conn_params)
    print(f"Establishing {conn_params['type']} connection on {conn_string}...")

    # 嘗試建立連接
    try:
        return mavutil.mavlink_connection(conn_string)
    except Exception as e:
        handle_connection_error(e, conn_params)

def construct_conn_string(conn_params):
    # 根据连接类型构造连接字符串
    if conn_params['type'] == 'udp':
        return f"udp:{conn_params['address']}:{conn_params['port']}"
    elif conn_params['type'] == 'serial':
        # 确保串行连接字符串格式为 "串口地址,波特率"
        return f"{conn_params['address']},{conn_params['baudrate']}"
    else:
        raise ValueError(f"Unsupported connection type: {conn_params['type']}")


def handle_connection_error(error, conn_params):
    # 特定錯誤處理
    if isinstance(error, socket.gaierror):
        print(f"Address resolution error for {conn_params['address']}: {error}")
    elif isinstance(error, socket.error):
        if error.errno == socket.errno.EACCES:
            print(f"Insufficient permissions to bind to port {conn_params['port']}.")
        elif error.errno == socket.errno.EADDRINUSE:
            print(f"Port {conn_params['port']} is already in use.")
        else:
            print(f"Socket error: {error}")
    else:
        print(f"Failed to establish connection: {error}")

    raise error  # 重新拋出錯誤以允許上層處理

def get_gps_data(vehicle):
    gps_data = vehicle.recv_match(type='GPS_RAW_INT', blocking=True, timeout=10)

    if gps_data:
        print(gps_data)
        fix_type = gps_data.fix_type
        if fix_type == 3:
            print("3D Fix")
        elif fix_type == 6:
            print("RTK Fixed")
        else:
            print(f"Other GPS Fix Type: {fix_type}")
    else:
        status_text = vehicle.recv_match(type='STATUS_TEXT', blocking=True, timeout=10)
        if status_text:
            if "RTK" in status_text.text:
                print("RTK status detected from STATUS_TEXT!")
            elif "3D Fix" in status_text.text:
                print("3D Fix status detected from STATUS_TEXT!")
        else:
            print("No GPS data or status received.")


# Load connection parameters from a JSON file
try:
    print("Loading connection parameters...")
    with open('config.json', 'r') as f:
        params = json.load(f)
except FileNotFoundError:
    print("Config file not found. Exiting.")

# Initialize the connections
heli = None
rover = None

try:
    print("Establishing connections...")
    heli = create_connection(params['heli'])
    rover = create_connection(params['rover'])
except Exception as e:
    print(f"Failed to establish connection: {e}")
    exit(1)  # Exit if we cannot establish a connection

# Ensure that both heli and rover are connected before proceeding
if heli is None or rover is None:
    print("One or more connections could not be established. Exiting.")
    exit(1)

# The rest of your code for the MAVLink protocol...


    
# Request the GPS_RAW_INT message stream from the rover at a higher rate (e.g., 5Hz)
rover.mav.request_data_stream_send(rover.target_system, rover.target_component,
                                   mavutil.mavlink.MAV_DATA_STREAM_POSITION, 5, 1)






# (If needed) Take off and switch to FOLLOW mode
# Uncomment the following lines if required:
"""
heli.mav.command_long_send(
    heli.target_system, heli.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,
    0, 0, 0, 0, 0, 0, 10  # Take-off altitude set to 10m
)
time.sleep(1)  # Allow some time for take-off

# Switch to FOLLOW mode
heli.set_mode(mavutil.mavlink.COPTER_MODE_FOLLOW)
"""

initial_location = heli.location()
initial_lat = initial_location.lat
initial_lon = initial_location.lng  


heli.mav.param_set_send(
    heli.target_system, 
    heli.target_component, 
    b'FOLL_YAW_BEHAVE', 
    0,
    mavutil.mavlink.MAV_PARAM_TYPE_INT8
)

# 設置新的家庭點座標
#  
new_home_latitude = 25.03338490  # 緯度，以度為單位
new_home_longitude = 121.56551376  # 經度，以度為單位
new_home_altitude = 0.0       # 高度，以米為單位

while True:
    # Get the current location of the heli and rover
    rover_location = rover.location()
    heli_location = heli.location()

    # Print the current location of the heli and rover
    get_gps_data(heli)
    get_gps_data(rover)
   

    # 接收并打印心跳包
    #heli_heartbeat = heli.recv_match(type='HEARTBEAT', blocking=False)
    #rover_heartbeat = rover.recv_match(type='HEARTBEAT', blocking=False)
    #if heli_heartbeat:
        #print("Heli Heartbeat:", heli_heartbeat)
    #if rover_heartbeat:
        #print("Rover Heartbeat:", rover_heartbeat)

    
    #print("Heli location:", heli_location.lat, heli_location.lng,get_current_yaw(heli))
    rover_cal_yaw_lat,rover_cal_yaw_lng=calculate_new_coordinates(heli_location.lat, heli_location.lng,get_current_yaw(heli), 25)
    heli_cal_yaw_lat,heli_cal_yaw_lng=calculate_new_coordinates(rover_location.lat, rover_location.lng,get_current_yaw(rover), 25)

    time_boot_ms = int(time.time() * 1000) % 4294967296
    
    print("Time Boot MS:", int(time.time() * 1000))
    print("Rover Lat:", int(rover_location.lat * 1e6), "Heli Lat:", int(heli_location.lat * 1e6))
    print("Rover lng:", int(rover_location.lng * 1e6), "Heli lng:", int(heli_location.lng * 1e6))
    print("Rover alt:", int(rover_location.alt ),"m.", "Heli alt:", int(heli_location.alt ),"m.")

    # Set the fetched target location as the HOME point
    
    #print("Heli location to Rover Setting home point...")
    set_home_position(rover,rover_cal_yaw_lat, rover_cal_yaw_lng, 0)
    #print("Rover location to Heli Setting home point...")
    set_home_position(heli,heli_cal_yaw_lat, heli_cal_yaw_lng, 0)


    
    time.sleep(1)  # Update location information every second


keyboard_thread.join()
