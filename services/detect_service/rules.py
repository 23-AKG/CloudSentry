from collections import defaultdict
from datetime import datetime, timedelta

# Store failed login timestamps by IP
failed_logins = defaultdict(list)

def check_brute_force(event):
    if event["event"] != "failed_login":
        return None

    ip = event["ip"]
    ts = datetime.fromisoformat(event["timestamp"])
    failed_logins[ip].append(ts)

    # Keep only attempts in the last 30 seconds
    failed_logins[ip] = [t for t in failed_logins[ip] if ts - t <= timedelta(seconds=30)]

    if len(failed_logins[ip]) >= 3:
        return {
            "alert": "Brute Force Detected",
            "ip": ip,
            "count": len(failed_logins[ip]),
            "last_seen": ts.isoformat()
        }
    return None
