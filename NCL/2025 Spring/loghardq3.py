import struct

def count_unique_usernames(filename):
    unique_usernames = set()
    with open(filename, 'rb') as f:
        while True:
            # 1) Read username_length
            raw = f.read(4)
            if len(raw) < 4:
                break  # EOF
            (username_length,) = struct.unpack('>I', raw)

            # 2) Read the username bytes and decode as UTF-8
            username_bytes = f.read(username_length)
            username = username_bytes.decode('utf-8', errors='ignore')

            # 3) Add to our set
            unique_usernames.add(username)

            # 4) Skip IP (4), timestamp (4), success flag (1)
            f.seek(4 + 4 + 1, 1)

    return len(unique_usernames)

if __name__ == '__main__':
    num_unique = count_unique_usernames('logins.bin')
    print("Unique usernames:", num_unique)
