import socket
import threading
import time

def test_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', port))
        sock.listen(1)
        print(f"✅ Port {port} is available!")
        sock.close()
        return True
    except Exception as e:
        print(f"❌ Port {port} failed: {e}")
        return False

# Test common ports
ports_to_test = [3000, 8000, 8080, 8081, 8082, 8083, 9000, 12345, 54321]

print("Testing available ports...")
available_ports = []

for port in ports_to_test:
    if test_port(port):
        available_ports.append(port)

print(f"\n🎯 Available ports: {available_ports}")

if available_ports:
    print(f"✅ Use port {available_ports[0]} for your server!")
else:
    print("❌ No ports available. Check your firewall/antivirus settings.")
