import psutil
import socket

def get_active_connections():
    """
    Get a list of active network connections on the endpoint.
    """
    connections = psutil.net_connections(kind='inet')
    active_connections = []

    for conn in connections:
        if conn.status == 'ESTABLISHED' or conn.status == 'SYN_SENT':
            local_ip, local_port = conn.laddr
            remote_ip, remote_port = conn.raddr if conn.raddr else ("Unknown", "Unknown")
            process_info = psutil.Process(conn.pid) if conn.pid else None
            app_name = process_info.name() if process_info else "Unknown"

            active_connections.append({
                "local_ip": local_ip,
                "local_port": local_port,
                "remote_ip": remote_ip,
                "remote_port": remote_port,
                "app_name": app_name,
                "protocol": "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
            })

    return active_connections

def monitor_traffic():
    """
    Continuously monitor network traffic.
    """
    while True:
        active_connections = get_active_connections()
        for conn in active_connections:
            print(f"App: {conn['app_name']}, Local IP: {conn['local_ip']}, Remote IP: {conn['remote_ip']}, Protocol: {conn['protocol']}")
        # Add a sleep interval to control the monitoring frequency
        time.sleep(1)
