import bluetooth
import subprocess
import threading

def discover_devices():
    """Discover nearby Bluetooth devices."""
    print("Discovering nearby Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    devices = []
    for addr, name in nearby_devices:
        print(f"Found device: {name} with address: {addr}")
        devices.append((addr, name))
    return devices

def pair_device(address):
    """Pair with a Bluetooth device using bluetoothctl."""
    try:
        print(f"Pairing with device: {address}")
        process = subprocess.Popen(['bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate(input=f'pair {address}\n'.encode())
        process.communicate(input='yes\n'.encode())
        process.communicate(input=f'trust {address}\n'.encode())
        process.communicate(input=f'connect {address}\n'.encode())
        print(f"Paired with device: {address}")
    except Exception as e:
        print(f"Failed to pair with device: {address}, Error: {str(e)}")

def handle_device_connection(address):
    """Handle the connection with a Bluetooth device."""
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
        sock.connect((address, port))
        print(f"Connected to {address}")
        
        # Example data exchange
        sock.send("Hello, Bluetooth!")
        data = sock.recv(1024)
        print(f"Received from {address}: {data}")
    except Exception as e:
        print(f"Failed to connect to {address}, Error: {str(e)}")
    finally:
        sock.close()

def main():
    devices = discover_devices()
    
    # Pair with each discovered device
    for address, name in devices:
        pair_device(address)
    
    # Connect to each paired device in a separate thread
    threads = []
    for address, name in devices:
        thread = threading.Thread(target=handle_device_connection, args=(address,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()