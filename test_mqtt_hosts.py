#!/usr/bin/env python3
"""
Script pour tester différents hostnames MQTT
"""
import socket
import ssl

# Liste des hostnames à tester
hosts = [
    "api.iot.thermomaven.com",
    "mqtt.iot.thermomaven.com",
    "emqx.iot.thermomaven.com",
    "broker.iot.thermomaven.com",
    "iot.thermomaven.com",
]

ports = [8883, 1883, 8884]

print("="*70)
print("Testing MQTT broker hostnames...")
print("="*70)

for host in hosts:
    print(f"\n[*] Testing {host}...")
    
    # Test DNS resolution
    try:
        ip = socket.gethostbyname(host)
        print(f"  [+] DNS resolves to: {ip}")
        
        # Test connection on different ports
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                
                result = sock.connect_ex((host, port))
                
                if result == 0:
                    print(f"  [+] Port {port} is OPEN")
                    
                    # If port 8883, try SSL handshake
                    if port == 8883:
                        try:
                            context = ssl.create_default_context()
                            context.check_hostname = False
                            context.verify_mode = ssl.CERT_NONE
                            
                            with socket.create_connection((host, port), timeout=3) as sock:
                                with context.wrap_socket(sock, server_hostname=host) as ssock:
                                    print(f"    [+] SSL handshake successful")
                                    print(f"    SSL version: {ssock.version()}")
                        except Exception as e:
                            print(f"    [!] SSL handshake failed: {e}")
                else:
                    print(f"  [-] Port {port} is CLOSED or filtered")
                
                sock.close()
                
            except socket.timeout:
                print(f"  [!] Port {port} timeout")
            except Exception as e:
                print(f"  [-] Port {port} error: {e}")
                
    except socket.gaierror:
        print(f"  [-] DNS resolution failed")
    except Exception as e:
        print(f"  [-] Error: {e}")

print("\n" + "="*70)
print("Summary:")
print("="*70)
print("The MQTT broker should be the host with:")
print("  - Successful DNS resolution")
print("  - Port 8883 OPEN (MQTT over SSL/TLS)")
print("  - Successful SSL handshake")

