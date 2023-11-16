from pymavlink import mavutil
import math

# 创建与飞行器的UDP连接
master = mavutil.mavlink_connection('udp:127.0.0.1:14551')

def check_connection(master, timeout=5):
    try:
        # 等待心跳消息
        master.wait_heartbeat(timeout=timeout)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_location(master):
    """获取当前坐标"""
    return master.location()


def set_home_with_offset(master, offset_meters=50):
    """获取当前坐标，添加offset，并设置为home点"""
    current_location = get_location(master)
    
    # 计算偏移量
    # 注意：这是一个简化的计算方法，实际上地球是一个椭球体
    offset_latitude = offset_meters / 111319.5
    offset_longitude = offset_meters / (111319.5 * abs(math.cos(current_location.lat)))
    
    new_lat = current_location.lat + offset_latitude
    new_lon = current_location.lng + offset_longitude  # 注意这里修改为lng
    new_alt = current_location.alt  # 保持当前的高度
    
    # 更新home点
    master.mav.command_long_send(
        master.target_system,  # target_system
        master.target_component,  # target_component
        mavutil.mavlink.MAV_CMD_DO_SET_HOME,  # command
        0,  # confirmation
        0,  # use current location
        0, 0, 0,  # reserved
        new_lat,  # latitude
        new_lon,  # longitude
        new_alt  # altitude
    )

is_connected = check_connection(master)

if is_connected:
    print("Successfully connected!")
    
    # 获取坐标，添加偏移量，并更新home点
    set_home_with_offset(master)
    print("Home point updated with offset.")
    
else:
    print("Failed to connect or no heartbeat received.")
