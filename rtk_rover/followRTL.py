from pymavlink import mavutil
import time
import math
import json
import socket



# Establish a connection with the aircraft
#master = mavutil.mavlink_connection('udp:127.0.0.1:14551')
# Establish a connection with the Rover ground station
#rover = mavutil.mavlink_connection('udp:127.0.0.1:14552')


from pymavlink import mavutil
import json
import socket

# Function to create a mavlink connection based on the type
def create_connection(conn_params):
    if conn_params['type'] == 'udp':
        conn_string = f"udp:{conn_params['address']}:{conn_params['port']}"
    elif conn_params['type'] == 'serial':
        conn_string = f"{conn_params['address']}:{conn_params['baudrate']}"
    else:
        raise ValueError(f"Unsupported connection type: {conn_params['type']}")

    try:
        return mavutil.mavlink_connection(conn_string)
    except socket.gaierror as e:
        print(f"Address resolution error for {conn_params['address']}: {e}")
        raise
    except socket.error as e:
        if e.errno == socket.errno.EACCES:
            print(f"Insufficient permissions to bind to port {conn_params['port']}.")
        elif e.errno == socket.errno.EADDRINUSE:
            print(f"Port {conn_params['port']} is already in use.")
        else:
            print(f"Socket error: {e}")
        raise

# Load connection parameters from a JSON file
with open('config.json', 'r') as f:
    params = json.load(f)

# Initialize the connections
master = None
rover = None

try:
    master = create_connection(params['master'])
    rover = create_connection(params['rover'])
except Exception as e:
    print(f"Failed to establish connection: {e}")
    exit(1)  # Exit if we cannot establish a connection

# Ensure that both master and rover are connected before proceeding
if master is None or rover is None:
    print("One or more connections could not be established. Exiting.")
    exit(1)

# The rest of your code for the MAVLink protocol...


    
# Request the GPS_RAW_INT message stream from the rover at a higher rate (e.g., 5Hz)
rover.mav.request_data_stream_send(rover.target_system, rover.target_component,
                                   mavutil.mavlink.MAV_DATA_STREAM_POSITION, 5, 1)






# (If needed) Take off and switch to FOLLOW mode
# Uncomment the following lines if required:
"""
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,
    0, 0, 0, 0, 0, 0, 10  # Take-off altitude set to 10m
)
time.sleep(1)  # Allow some time for take-off

# Switch to FOLLOW mode
master.set_mode(mavutil.mavlink.COPTER_MODE_FOLLOW)
"""

initial_location = master.location()
initial_lat = initial_location.lat
initial_lon = initial_location.lng  

radius = 5 # 大约等于100m


angle = 0  # 初始化角度


master.mav.param_set_send(
    master.target_system, 
    master.target_component, 
    b'FOLL_YAW_BEHAVE', 
    0,
    mavutil.mavlink.MAV_PARAM_TYPE_INT8
)



while True:

    # Fetch the location of the rover to serve as the target location for the aircraft
    rover_location = rover.location()
    target_lat = rover_location.lat
    target_lon = rover_location.lng

    #for testing
    target_lat = initial_lat + radius * math.sin(math.radians(angle)) / 111319.9  # 111319.9 是地球上每度纬度的大约距离（以米为单位）
    target_lon = initial_lon + radius * math.cos(math.radians(angle)) / 111319.9
    angle += 3  # 增加角度，使目标沿圆圈移动
    if angle >= 360:
        angle = 0  # 重置角度

    

    gps_data = rover.recv_match(type='GPS_RAW_INT', blocking=True, timeout=10)
    
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
        status_text = rover.recv_match(type='STATUS_TEXT', blocking=True, timeout=10)
        if status_text:
            if "RTK" in status_text.text:
                print("RTK status detected from STATUS_TEXT!")
            elif "3D Fix" in status_text.text:
                print("3D Fix status detected from STATUS_TEXT!")
        else:
            print("No GPS data or status received.")

    time_boot_ms = int(time.time() * 1000) % 4294967296
    
    print("Time Boot MS:", int(time.time() * 1000))
    print("Target Lat:", int(target_lat * 1e7))
    print("Target Lon:", int(target_lon * 1e7))
    print("Alt:", 1000)
    print("Relative Alt:", 0)
    print("VX:", 0)
    print("VY:", 0)
    print("VZ:", 0)
    print("HDG:", 0)
    # Set the fetched target location as the HOME point
    print("Setting home point...")
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_HOME, 0, 1, 0, 0, 0,
        target_lat, target_lon, 0  # Altitude remains at 10m
    )
    
    # Transmit the target location to the aircraft
    print("Sending target location...")
    master.mav.global_position_int_send(
        time_boot_ms,                # Using the corrected value
        int(target_lat * 1e7),      # Latitude
        int(target_lon * 1e7),      # Longitude
        1000,                       # Altitude (in centimeters)
        0, 0, 0, 0, 0, 0            # Other parameters such as velocity and direction
    )

    time.sleep(1)  # Update location information every second
