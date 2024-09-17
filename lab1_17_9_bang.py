import subprocess

def run_snmp_command(command):
    """Runs an SNMP command using subprocess and returns the output."""
    try:
        # Run the SNMP command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Check if the command was successful
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error running command: {command}\n{result.stderr}")
            return None
    except Exception as e:
        print(f"Exception occurred while running command {command}: {e}")
        return None

def get_router_name(target):
    """Fetches the router name (sysName) using snmpget."""
    command = f"snmpget -v1 -c public {target} 1.3.6.1.2.1.1.5.0"
    output = run_snmp_command(command)
    if output:
        # Split by '=' and strip any extra spaces to get the value
        return output.split('=')[-1].strip()
    return None

def get_interface_names(target):
    """Fetches the names of all interfaces (ifDescr) using snmpwalk."""
    command = f"snmpwalk -v1 -c public {target} 1.3.6.1.2.1.2.2.1.2"
    output = run_snmp_command(command)
    if output:
        # Parse each line, split by '=', and strip to get the interface names
        return {
            line.split('=')[0].split('.')[-1].strip(): line.split('=')[-1].strip()
            for line in output.split('\n') if '=' in line
        }
    return {}

def get_interface_bandwidths(target):
    """Fetches the bandwidth of all interfaces (ifSpeed) using snmpwalk."""
    command = f"snmpwalk -v1 -c public {target} 1.3.6.1.2.1.2.2.1.5"
    output = run_snmp_command(command)
    if output:
        # Parse each line, split by '=', and strip to get the bandwidth values
        return {
            line.split('=')[0].split('.')[-1].strip(): line.split('=')[-1].strip()
            for line in output.split('\n') if '=' in line
        }
    return {}

# Define the IP address of your Cisco 7200 router
target_ip = '192.168.17.130'  # Replace with the actual IP address of your router

# 1. Check Router Name
router_name = get_router_name(target_ip)
if router_name:
    print(f"Router Name: {router_name}")

# 2. Check Interface Names
interface_names = get_interface_names(target_ip)
for index, name in interface_names.items():
    if name:  # Only print if name is not empty
        print(f"Interface {index}: {name}")

# 3. Check Bandwidth for Each Interface
interface_bandwidths = get_interface_bandwidths(target_ip)
for index, bandwidth in interface_bandwidths.items():
    if bandwidth:  # Only print if bandwidth is not empty
        print(f"Interface {index} Bandwidth: {bandwidth} bps")
