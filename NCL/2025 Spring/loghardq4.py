import struct
import socket

def count_unique_ips(filename):
    unique_ips = set()
    with open(filename, 'rb') as f:
        while True:
            # Read username_length
            raw = f.read(4)
            if len(raw) < 4:
                break
            (username_length,) = struct.unpack('>I', raw)

            # Skip the username bytes
            f.seek(username_length, 1)

            # Read the 4-byte IP address
            ip_bytes = f.read(4)
            if len(ip_bytes) < 4:
                break
            # Convert to dotted quad
            ip_str = socket.inet_ntoa(ip_bytes)
            unique_ips.add(ip_str)

            # Skip timestamp (4) and success (1)
            f.seek(4 + 1, 1)

    return len(unique_ips)

if __name__ == '__main__':
    num_ips = count_unique_ips('logins.bin')
    print("Unique IP addresses:", num_ips)
