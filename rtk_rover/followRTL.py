from pymavlink import mavutil
import time
import math
import json
import socket

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
    # 根據連接類型構造連接字符串
    if conn_params['type'] == 'udp':
        return f"udp:{conn_params['address']}:{conn_params['port']}"
    elif conn_params['type'] == 'serial':
        return f"{conn_params['address']}:{conn_params['baudrate']}"
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
new_home_latitude = 47.3977415  # 緯度，以度為單位
new_home_longitude = 8.5455934  # 經度，以度為單位
new_home_altitude = 488.0       # 高度，以米為單位

while True:

    rover_location = rover.location()
    heli_location = heli.location()

    
    get_gps_data(rover)
    get_gps_data(heli)

    time_boot_ms = int(time.time() * 1000) % 4294967296
    
    print("Time Boot MS:", int(time.time() * 1000))
    print("Rover Lat:", int(rover_location.lat * 1e6), "Heli Lat:", int(heli_location.lat * 1e6))
    print("Rover lng:", int(rover_location.lng * 1e6), "Heli lng:", int(heli_location.lng * 1e6))
    print("Rover alt:", int(rover_location.alt ),"m.", "Heli alt:", int(heli_location.alt ),"m.")

    # Set the fetched target location as the HOME point
    print("Heli location to Rover Setting home point...")
    heli.mav.command_long_send(
        heli.target_system, heli.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_HOME,
        0,            # 確認
        0,            # 參數1，1=使用當前位置，0=使用指定的經緯度
        0, 0, 0,      # 參數2, 3, 4 不使用
        rover_location.lat, rover_location.lng, new_home_altitude
    )
    print("Rover location to Heli Setting home point...")
    rover.mav.command_long_send(
        rover.target_system, rover.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_HOME,
        0,            # 確認
        0,            # 參數1，1=使用當前位置，0=使用指定的經緯度
        0, 0, 0,      # 參數2, 3, 4 不使用
        heli_location.lat, heli_location.lng, new_home_altitude
    )
    
    time.sleep(1)  # Update location information every second
