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
import os
from os import startfile

# Build tracker client, to establish a communication with the tracker server (an Eyeware application).
#
# Constructing the tracker client object without arguments sets a default server hostname and port which
# work fine in many configurations.
# However, it is possible to set a specific hostname and port, depending on your setup and network.
# See the TrackerClient API reference for further information.
tracker = TrackerClient()

# Name und Datum für den späteren Export
name = input("Enter Name_Datum:")

# Startet das Video (Vorher Video öffnen)
startfile("Conjuring2_0.mp4")

# Timer in Sekunden
start_time = time.time()

# Timer wie lang das Skript läuft, orientiert an der Videolänge
Timeout = time.time() + (3.31 * 60)

# Löscht den alten DataFrame, wenn vorhanden
try:
    del df
except NameError:
    pass

df = pd.DataFrame({'Timestamp': [], 'Gaze X': [], 'Gaze Y': [], "Lost Track": [], "Confidence": []})  # DataFrame

# Run forever, until we press ctrl+c/Strg + F2
try:
    while time.time() < Timeout:
        # Make sure that the connection with the tracker server (Eyeware application) is up and running.
        if tracker.connected:

            print("  * Gaze on Screen:")
            screen_gaze = tracker.get_screen_gaze_info()
            screen_gaze_is_lost = screen_gaze.is_lost
            print("      - Lost track:       ", screen_gaze_is_lost)
            if screen_gaze_is_lost:
                df = df.append({"Lost Track": screen_gaze_is_lost, 'Timestamp': "%s" % (time.time() - start_time)}, ignore_index=True)
            if not screen_gaze_is_lost:
                print("      - Coordinates:       <x=%5.3f px,   y=%5.3f px>" % (screen_gaze.x, screen_gaze.y))
                print("      - Confidence:       ", screen_gaze.confidence)
                print("      - Timestamps:          %s     " % (time.time() - start_time))
                df = df.append({'Timestamp': "%s" % (time.time() - start_time), "Gaze X": "%5.3f" % (screen_gaze.x),
                                'Gaze Y': "%5.3f" % (screen_gaze.y),
                                "Confidence": screen_gaze.confidence}, ignore_index=True)

            time.sleep(1 / 120)  # We expect tracking data at 120 Hz
        else:
            # Print a message every MESSAGE_PERIOD_IN_SECONDS seconds
            MESSAGE_PERIOD_IN_SECONDS = 2
            time.sleep(MESSAGE_PERIOD_IN_SECONDS - time.monotonic() % MESSAGE_PERIOD_IN_SECONDS)
            print("No connection with tracker server")
except KeyboardInterrupt:
    pass

print(df)

# Löscht csv Dateien mit denselben Namen
if os.path.exists(name + ".csv"):
    os.remove(name + ".csv")
    print("The file has been deleted successfully")
else:
    print("The file does not exist!")

# Export
df.to_csv("Daten/" + name + ".csv")
