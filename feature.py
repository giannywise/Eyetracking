# Sammlung an Funktion für Feature generation

import math
import pandas as pd
import numpy as np
import time
import os
import matplotlib.pyplot as plt


# Generiert Fixiation
def fix(df):
    df_fix = pd.DataFrame({'Fixation': []})
    f = 1
    for i in range(len(df)):
        try:
            j = i + 1
            k = j + 1
            if np.sqrt((df.iloc[i]['Gaze X'] - df.iloc[j]['Gaze X']) ** 2) <= 40 and np.sqrt(
                    (df.iloc[i]['Gaze Y'] - df.iloc[j]['Gaze Y']) ** 2) <= 40:
                df_fix = df_fix.append({'Fixation': f}, ignore_index=True).astype(int)
            else:
                df_fix = df_fix.append({'Fixation': 0}, ignore_index=True).astype(int)
                if np.sqrt((df.iloc[j]['Gaze X'] - df.iloc[k]['Gaze X']) ** 2) <= 40 and np.sqrt(
                        (df.iloc[j]['Gaze Y'] - df.iloc[k]['Gaze Y']) ** 2) <= 40:
                    f += 1
                else:
                    pass
        except IndexError:
            df_fix = df_fix.append({'Fixation': 0}, ignore_index=True).astype(int)
    df_fix = df_fix.shift(periods=1, axis=0, fill_value= 1)
    #d = df['Fixation'] = df_fix
    #d['Fixation'] = d['Fixation'].notna().astype(int)
    return df_fix

# Generiert Geschwindigkeiten
# dx & dy = differenz. d = Abstand, vx & vy = Geschwindigkeit in x & y Richtung [px/s],
# v = Betrag des Geschwindigkeitsvektor [px/s], a = Richtung, omega = winkelgeschwindigkeit
def ges(df):
    try:
        del df_rad
    except NameError:
        pass
    df_rad = pd.DataFrame({'dx': [], 'dy': [], 'd': [], 'vx': [], 'vy': [], 'v': [], 'a': []})
    # df[] = df[]
    for i in range(len(df)):
        try:
            j = i + 1
            t = df.iloc[j]['Timestamp'] - df.iloc[i]['Timestamp']
            dx = df.iloc[j]['Gaze X'] - df.iloc[i]['Gaze X']
            dy = df.iloc[j]['Gaze Y'] - df.iloc[i]['Gaze Y']
            d = np.sqrt(dx ** 2 + dy ** 2)
            v = d / t
            if dx == 0 and dy == 0:
                v = 0
                vx = 0
                vy = 0
                a = 0
            elif dx == 0 and dy != 0:
                vy = v
                vx = 0
                a = 0
            elif dy == 0 and dx != 0:
                vx = v
                vy = 0
                a = np.pi / 2
            else:
                m = dy / dx
                a = np.arcsin(dx / d)
                vx = v * np.sin(a)
                vy = v * np.cos(a)
            # print(int(vx),int(vy),int(v))

            df_rad = df_rad.append(
                {'dx': int(dx), 'dy': int(dy), 'd': int(d), 'vx': int(vx), 'vy': int(vy), 'v': int(v), 'a': int(a)},
                ignore_index=True)
        except IndexError:
            pass
    return df_rad
