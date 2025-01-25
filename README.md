# waybar-dexcom

This is a custom module for waybar which displays your current blood glucose levels from the Dexcom SHARE service. Theoretically, it should work for any CGM with support for Dexcom SHARE.\
![pydexcom](https://github.com/Narmis-E/waybar-dexcom/assets/109248529/b521c098-3da1-48c5-9be0-d585ca504374)

Make sure to add in your SHARE username and password into the file:

```
#! /usr/bin/python3

from pydexcom import Dexcom

def calculate_delta(current_bg, previous_bg):
    return current_bg - previous_bg

dexcom = Dexcom(username="USERNAME HERE", passowrd="PASWORD HERE") # region="ous" if outside US

latest_readings = dexcom.get_glucose_readings(minutes=10, max_count=2)
current_bg_value = latest_readings[0].mmol_l
previous_bg_value = latest_readings[1].mmol_l

delta = calculate_delta(current_bg_value, previous_bg_value)
delta_str = f"{'' if delta == 0 else ('+' if delta > 0 else '-')} {abs(delta):.1f}"
delta_str = delta_str.replace(" ", "")

print(f'{{"text":"{current_bg_value:.1f} {latest_readings[0].trend_arrow}", "tooltip":"{delta_str}"}}')

```

Then running it through waybar can be done as follows:

```
"custom/dexcom": {
    "format": "<span color=\"#F7768E\"></span> {}",
    "return-type": "json",
    "exec": "python3 {PATH TO dexcom.py}",
    "interval": 1,
    "tooltip": "true"
  },
```

Each time the bg updates, the module will dissapear for a few seconds as the api is retrieving a new bg reading.\
If you can think of any ways to improve this please feel welcome to make a pr. [Gagebenne's](https://github.com/gagebenne) pydexcom api provides the possibility for some more functionality, which can be found [here](https://gagebenne.github.io/pydexcom/pydexcom.html).\

For more complete experience, see my other project: [DexViewer](https://github.com/narmis-e/dexviewer).
 
