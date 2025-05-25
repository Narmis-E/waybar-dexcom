#! /usr/bin/python3

from pydexcom import Dexcom

def calculate_delta(current_bg, previous_bg):
    return current_bg - previous_bg

dexcom = Dexcom(username="username", password="password", region="ous")

try:
    latest_readings = dexcom.get_glucose_readings(minutes=10, max_count=2)
    if len(latest_readings) >= 2:
        current_bg_value = latest_readings[0].mmol_l
        previous_bg_value = latest_readings[1].mmol_l

        delta = calculate_delta(current_bg_value, previous_bg_value)
        delta_str = f"{'' if delta == 0 else ('+' if delta > 0 else '-')} {abs(delta):.1f}".replace(" ", "")

        print(f'{{"text":"{current_bg_value:.1f} {latest_readings[0].trend_arrow}", "tooltip":"{delta_str}"}}')
    else:
        print('{"text":"---", "tooltip":"No readings available"}')
except Exception as e:
    print('{"text":"---", "tooltip":"Error retrieving data"}')
