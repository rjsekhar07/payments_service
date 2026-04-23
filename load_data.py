import json
import requests
import time

URL = "http://127.0.0.1:8000/events"

with open("sample_events.json") as f:
    events = json.load(f)

success = 0
duplicate = 0
failed = 0

for i, event in enumerate(events):
    try:
        response = requests.post(URL, json=event, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "duplicate":
                duplicate += 1
            else:
                success += 1
        else:
            print(f"FAILED: {response.status_code}, {response.text}")
            failed += 1

        # 🔥 ADD THIS (VERY IMPORTANT)
        time.sleep(0.01)

        if i % 1000 == 0:
            print(f"{i} events processed...")

    except Exception as e:
        print("Error:", e)
        failed += 1

print("\n==== LOAD SUMMARY ====")
print(f"Success: {success}")
print(f"Duplicates: {duplicate}")
print(f"Failed: {failed}")