import subprocess
import os

def snmpwalk(target, oid):
    snmpwalk_path = r'C:\usr\bin\snmpwalk.exe'  # ปรับเส้นทางนี้ให้ตรงกับที่ติดตั้ง
    try:
        result = subprocess.run(
            [snmpwalk_path, '-v', '2c', '-c', 'public', target, oid],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e}\nOutput: {e.output}\nError Output: {e.stderr}"

def parse_interface_speed(output):
    lines = output.splitlines()
    speeds = {}
    for line in lines:
        if 'Gauge32' in line:
            parts = line.split(' = Gauge32: ')
            if len(parts) == 2:
                oid, value = parts
                value = value.strip()
                if value == '4294967295':
                    speed = 'N/A'
                else:
                    speed = f"{int(value) / 1_000_000} Mbps"  # Convert to Mbps
                speeds[oid] = speed
    return speeds

def main():
    target_ip = '192.168.17.130'

    # ตรวจสอบชื่ออุปกรณ์
    print("Router Name:")
    router_name = snmpwalk(target_ip, '1.3.6.1.2.1.1.5.0')
    print(router_name)

    # ตรวจสอบชื่ออินเตอร์เฟส
    print("Interface Names:")
    interface_names = snmpwalk(target_ip, '1.3.6.1.2.1.2.2.1.2')
    print(interface_names)

    # ตรวจสอบแบนด์วิดธ์
    print("Interface Speed:")
    interface_speed = snmpwalk(target_ip, '1.3.6.1.2.1.2.2.1.5')
    parsed_speed = parse_interface_speed(interface_speed)
    for oid, speed in parsed_speed.items():
        print(f"{oid}: {speed}")

if _name_ == "_main_":
    main()