# app.py
import os
import time
from datetime import datetime
from urllib.request import urlopen
import json
import socket


# File to store IP logs
LOG_FILE = "ip_log.txt"
WAIT_SECONDS = 60

def get_public_ip_old():
    """Fetch the IP address from the local TCP service."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((LOCAL_SERVICE_HOST, LOCAL_SERVICE_PORT))
            # Receive the IP address from the server
            ip = client_socket.recv(1024).decode("utf-8")
            return ip
    except Exception as e:
        print(f"Error fetching IP from local service: {e}")
        return None

def get_public_ip():
    try:
        hostname = "myip.opendns.com"
        resolver = "resolver1.opendns.com"
        
        # Perform a DNS query to get the public IP
        ip = socket.gethostbyname_ex(resolver)[2][0]
        return ip
    except Exception as e:
        return f"Error: {e}"
    
    
def log_ip_change(ip):
    """Log the IP address and timestamp to the file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - IP: {ip}\n"

    # Append the log entry to the file
    with open(LOG_FILE, "a") as file:
        file.write(log_entry)
    print(f"Logged: {log_entry.strip()}")

def get_all_previous_ips():
    """Retrieve all previous IPs from the file."""
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as file:
        lines = file.readlines()
        # Skip the header line (if it exists) and extract IPs
        ips = [line.strip() for line in lines if "IP: " in line]
    return ips

def display_previous_ips():
    """Display all previous IPs on startup."""
    previous_ips = get_all_previous_ips()
    if previous_ips:
        print("Previous IPs:")
        for ip_entry in previous_ips:
            print(ip_entry)
    else:
        print("No previous IPs found in the log file.")

def main():
    # Create the log file if it doesn't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as file:
            file.write("IP Change Log\n")
        print(f"Created log file: {LOG_FILE}")

    # Display all previous IPs on startup
    display_previous_ips()
    
    print(f"\nstarted checking for ip change every {WAIT_SECONDS} seconds.\n")

    try:
        while True:
            # Fetch the current public IP
            current_ip = get_public_ip()

            if current_ip:
                # Get the last logged IP
                previous_ips = get_all_previous_ips()
                last_logged_ip = None
                if previous_ips:
                    last_logged_ip = previous_ips[-1].split("IP: ")[1]

                # Log the IP only if it has changed
                if not last_logged_ip or current_ip != last_logged_ip:
                    log_ip_change(current_ip)

            else:
                print("Failed to fetch IP.")

            # Wait before starting again
            time.sleep(WAIT_SECONDS)
    except KeyboardInterrupt:
        print("\nProgram stopped.")

if __name__ == "__main__":
    main()
