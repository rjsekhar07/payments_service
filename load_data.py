import json
import requests
import time

URL = "https://payments-service-9o9x.onrender.com/events"

with open("sample_events.json") as f:
    events = json.load(f)

success = 0
duplicate = 0
failed = 0

def send_event(event, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(URL, json=event, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "duplicate":
                    return "duplicate"
                else:
                    return "success"
            else:
                print(f"FAILED: {response.status_code}, {response.text}")
        
        except requests.exceptions.RequestException:
            print(f"Retrying... ({attempt+1}/{retries})")
            time.sleep(0.5)

    return "failed"


for i, event in enumerate(events):
    result = send_event(event)

    if result == "success":
        success += 1
    elif result == "duplicate":
        duplicate += 1
    else:
        failed += 1

    # throttle requests (VERY IMPORTANT)
    time.sleep(0.01)

    if i % 1000 == 0:
        print(f"{i} events processed...")


print("\n==== LOAD SUMMARY ====")
print(f"Success: {success}")
print(f"Duplicates: {duplicate}")
print(f"Failed: {failed}")