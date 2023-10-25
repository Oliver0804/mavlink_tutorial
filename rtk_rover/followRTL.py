from pymavlink import mavutil
import time
import math

# 创建与飞行器的连接
master = mavutil.mavlink_connection('udp:127.0.0.1:14551')
# 创建Rover地面站的连接
rover = mavutil.mavlink_connection('udp:127.0.0.1:14552')

# 起飞并切换到FOLLOW模式
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,
    0, 0, 0, 0, 0, 0, 10  # 起飞高度为10m
)
time.sleep(1)  # 等待起飞

# 切换到FOLLOW模式
master.set_mode(mavutil.mavlink.COPTER_MODE_FOLLOW)

# 获取飞行器的起始位置
initial_location = master.location()
initial_lat = initial_location.lat
initial_lon = initial_location.lng  

radius = 5 # 大约等于100m


angle = 0  # 初始化角度

while True:

    
    # 获取rover的位置作为飞行器的目标位置
    rover_location = rover.location()
    print("rover_location:", rover_location)
    target_lat = rover_location.lat
    target_lon = rover_location.lng

    # 计算目标位置（沿圆圈移动）
    target_lat = initial_lat + radius * math.sin(math.radians(angle)) / 111319.9  # 111319.9 是地球上每度纬度的大约距离（以米为单位）
    target_lon = initial_lon + radius * math.cos(math.radians(angle)) / 111319.9

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
    
    # 设置目标位置为HOME点
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_HOME, 0, 1, 0, 0, 0,
        target_lat, target_lon, 0  # 高度保持为10m
    )
    
    # 向飞行器发送目标的位置信息
    master.mav.global_position_int_send(
        time_boot_ms,  # 使用修正后的值
        int(target_lat * 1e7),   # 纬度
        int(target_lon * 1e7),   # 经度
        1000,                    # 高度（单位：厘米）
        0, 0, 0, 0, 0, 0         # 其他参数，例如速度和方向
    )

    angle += 3  # 增加角度，使目标沿圆圈移动
    if angle >= 360:
        angle = 0  # 重置角度

    time.sleep(1)  # 每秒更新位置信息
