#!/usr/bin/env python3

import time
from datetime import datetime
from pydexcom import Dexcom

def calculate_delta(current_bg, previous_bg):
    return current_bg - previous_bg

def get_latest_readings(dexcom):
    try:
        return dexcom.get_glucose_readings(minutes=10, max_count=2)
    except Exception:
        return None

def main():
    dexcom = Dexcom(username="username", password="password", region="ous")
    last_seen_timestamp = None

    while True:
        readings = get_latest_readings(dexcom)

        if readings and len(readings) >= 2:
            latest, previous = readings[0], readings[1]

            # Compare timestamps to detect new reading
            if last_seen_timestamp != latest.datetime:
                last_seen_timestamp = latest.datetime

                current_bg = latest.mmol_l
                previous_bg = previous.mmol_l
                delta = calculate_delta(current_bg, previous_bg)

                delta_str = f"{'' if delta == 0 else ('+' if delta > 0 else '-')} {abs(delta):.1f}".replace(" ", "")
                print(f'{{"text":"{current_bg:.1f} {latest.trend_arrow}", "tooltip":"{delta_str}"}}', flush=True)
                
                # Wait 4m50s before checking again (usually catches reading blackout)
                time.sleep(290)
            else:
                # No new data yet, wait a little and try again
                time.sleep(10)
        else:
            # No readings available
            print('{"text":"---", "tooltip":"No readings available"}', flush=True)
            time.sleep(10)

if __name__ == "__main__":
    main()
