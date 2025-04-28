import struct
import datetime

def get_first_log_date(filename):
    with open(filename, 'rb') as f:
        # 1) Read username_length (4 bytes, big-endian unsigned int)
        raw = f.read(4)
        if len(raw) < 4:
            raise ValueError("File too short to contain a record.")
        (username_length,) = struct.unpack('>I', raw)

        # 2) Skip the username itself
        f.seek(username_length, 1)

        # 3) Skip the IP address (4 bytes)
        f.seek(4, 1)

        # 4) Read the timestamp (4 bytes, big-endian unsigned int)
        raw_ts = f.read(4)
        if len(raw_ts) < 4:
            raise ValueError("File ended before timestamp.")
        (ts,) = struct.unpack('>I', raw_ts)

        # 5) Convert to UTC datetime
        dt = datetime.datetime.utcfromtimestamp(ts)
        return dt.date()  # just the date portion

if __name__ == '__main__':
    first_date = get_first_log_date('logins.bin')
    print("Log starts on (UTC):", first_date.isoformat())
