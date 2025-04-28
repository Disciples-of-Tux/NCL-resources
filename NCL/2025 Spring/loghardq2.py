import struct

def count_login_events(filename):
    count = 0
    with open(filename, 'rb') as f:
        while True:
            # Read the 4-byte username_length
            raw = f.read(4)
            if len(raw) < 4:
                break  # EOF reached
            (username_length,) = struct.unpack('>I', raw)

            # Skip over the username, IP, timestamp, and success byte
            to_skip = username_length   # username
            to_skip += 4                # IPv4 address
            to_skip += 4                # timestamp
            to_skip += 1                # success flag

            # Move the file pointer forward
            f.seek(to_skip, 1)

            count += 1

    return count

if __name__ == '__main__':
    total_events = count_login_events('logins.bin')
    print("Total login-attempt events:", total_events)
