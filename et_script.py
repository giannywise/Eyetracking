"""
  Copyright (c) 2021 Eyeware Tech SA http://www.eyeware.tech

  This file provides an example on how to receive head and eye tracking data
  from Beam SDK.

  Dependencies:
  - Python 3.6
  - NumPy
"""

from eyeware.client import TrackerClient
import time
import datetime
from datetime import timedelta
import numpy as np
import pandas as pd

# Build tracker client, to establish a communication with the tracker server (an Eyeware application).
#
# Constructing the tracker client object without arguments sets a default server hostname and port which
# work fine in many configurations.
# However, it is possible to set a specific hostname and port, depending on your setup and network.
# See the TrackerClient API reference for further information.
tracker = TrackerClient()
start_time = time.time() #Timer in Sekunden

try:
    del df
except NameError:
    pass

df = pd.DataFrame({'Gaze X':[], 'Gaze Y':[], 'Timestamp': [] }) #DataFrame

# Run forever, until we press ctrl+c
for _ in range(1000):
    # Make sure that the connection with the tracker server (Eyeware application) is up and running.
    if tracker.connected:


        print("  * Gaze on Screen:")
        screen_gaze = tracker.get_screen_gaze_info()
        screen_gaze_is_lost = screen_gaze.is_lost
        print("      - Lost track:       ", screen_gaze_is_lost)
        if not screen_gaze_is_lost:
            print("      - Coordinates:       <x=%5.3f px,   y=%5.3f px>" % (screen_gaze.x, screen_gaze.y))
            print("      - Confidence:       ", screen_gaze.confidence)
            #print("      - Timestamps:       ", screen_gaze.confidence)
            print("      - Timestamps:          %s     " % (time.time() - start_time))
            df = df.append({"Gaze X": "%5.3f" % (screen_gaze.x), 'Gaze Y':"%5.3f" % (screen_gaze.y), 'Timestamp': "%s" % (time.time() - start_time)}, ignore_index = True)

        time.sleep(1 / 60)  # We expect tracking data at 60 Hz
    else:
        # Print a message every MESSAGE_PERIOD_IN_SECONDS seconds
        MESSAGE_PERIOD_IN_SECONDS = 2
        time.sleep(MESSAGE_PERIOD_IN_SECONDS - time.monotonic() % MESSAGE_PERIOD_IN_SECONDS)
        print("No connection with tracker server")

print(df)
name = input()
df.to_csv(name +".csv")