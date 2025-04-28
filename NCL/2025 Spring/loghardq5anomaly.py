#!/usr/bin/env python3
import struct
import socket
import datetime
import math
import csv
from collections import defaultdict

def compute_metrics(logfile, out_csv):
    # Accumulate per-user stats
    stats = defaultdict(lambda: {'total': 0, 'failures': 0, 'ips': set(), 'odd_hours': 0})
    total_attempts = total_failures = 0

    with open(logfile, 'rb') as f:
        while True:
            raw = f.read(4)
            if len(raw) < 4:
                break
            (uname_len,) = struct.unpack('>I', raw)
            uname = f.read(uname_len).decode('utf-8', errors='ignore')
            
            ip = socket.inet_ntoa(f.read(4))
            (ts,) = struct.unpack('>I', f.read(4))
            dt = datetime.datetime.utcfromtimestamp(ts)
            success = f.read(1) == b'\x01'

            s = stats[uname]
            s['total'] += 1
            total_attempts += 1
            if not success:
                s['failures'] += 1
                total_failures += 1
            s['ips'].add(ip)
            if dt.hour < 8 or dt.hour >= 18:
                s['odd_hours'] += 1

    # Global baseline failure rate
    p0 = total_failures / total_attempts

    # Write out CSV
    with open(out_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'username', 'total_attempts', 'failures', 'failure_rate',
            'unique_ips', 'odd_hours', 'z_score'
        ])
        for user, s in stats.items():
            n = s['total']
            k = s['failures']
            phat = k / n
            se = math.sqrt(p0 * (1 - p0) / n) if n > 0 else 0
            z = (phat - p0) / se if se > 0 else 0.0
            writer.writerow([
                user, n, k,
                f"{phat:.3f}",
                len(s['ips']),
                s['odd_hours'],
                f"{z:.2f}"
            ])

if __name__ == '__main__':
    compute_metrics('logins.bin', 'user_suspicious_metrics.csv')
    print("Metrics written to user_suspicious_metrics.csv")
