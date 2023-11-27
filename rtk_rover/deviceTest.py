from pymavlink import mavutil
import time
#mavproxy.py --master=/dev/ttyUSB0 --baudrate=57600 --out=udp:127.0.0.1:14571
# 設定串口和波特率
serial_port = "/dev/ttyACM1"
baud_rate = 115200

def main():
    # 建立與 MAVLink 設備的連接
    connection = mavutil.mavlink_connection(serial_port, baud=baud_rate)

    # 等待心跳包以確認連接
    print("Waiting for device heartbeats...")
    connection.wait_heartbeat()
    print("Heartbeat from system (system ID %u component ID %u)" % (connection.target_system, connection.target_component))

    # 讀取心跳包
    while True:
        try:
            msg = connection.recv_match(type='HEARTBEAT', blocking=True, timeout=5)
            if msg:
                print(f"Heartbeat received: {msg.to_dict()}")
            else:
                print("No heartbeat received. Check connection.")
        except KeyboardInterrupt:
            print("Exiting.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()
