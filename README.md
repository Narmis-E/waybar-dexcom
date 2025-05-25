# waybar-dexcom

This is a custom module for waybar which displays your current blood glucose levels from the Dexcom SHARE service. Theoretically, it should work for any CGM with support for Dexcom SHARE.\
![pydexcom](https://github.com/Narmis-E/waybar-dexcom/assets/109248529/b521c098-3da1-48c5-9be0-d585ca504374)

Make sure to add in your SHARE username and password into the file:

```
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


```

Then running it through waybar can be done as follows:

```
"custom/dexcom": {
    "format": "<span color=\"#F7768E\"></span> {}",
    "return-type": "json",
    "exec": "python3 {PATH TO dexcom.py}",
    "tooltip": "true"
  },
```

Each time the bg updates, the module will dissapear for a few seconds as the api is retrieving a new bg reading.\
If you can think of any ways to improve this please feel welcome to make a pr. [Gagebenne's](https://github.com/gagebenne) pydexcom api provides the possibility for some more functionality, which can be found [here](https://gagebenne.github.io/pydexcom/pydexcom.html).\

For more complete experience, see my other project: [DexViewer](https://github.com/narmis-e/dexviewer).
 
