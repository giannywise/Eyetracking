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
            p = i - 1
            j = i + 1
            k = j + 1
            d = 100  # absoluter Abstand
            try:
                if df.iloc[i]['Lost Track'] == 1:
                    df_fix = df_fix.append({'Fixation': 0}, ignore_index=True).astype(int)
                elif (np.sqrt((df.iloc[i]['Gaze X'] - df.iloc[j]['Gaze X']) ** 2) <= d \
                      and np.sqrt((df.iloc[i]['Gaze Y'] - df.iloc[j]['Gaze Y']) ** 2) <= d):
                    df_fix = df_fix.append({'Fixation': f}, ignore_index=True).astype(int)
                    if np.isnan() == True:
                        pass
                else:
                    df_fix = df_fix.append({'Fixation': 0}, ignore_index=True).astype(int)
                    if np.sqrt((df.iloc[j]['Gaze X'] - df.iloc[k]['Gaze X']) ** 2) <= d and np.sqrt(
                            (df.iloc[j]['Gaze Y'] - df.iloc[k]['Gaze Y']) ** 2) <= d:
                        f += 1
                        if np.isnan() == True:
                            pass
                    else:
                        pass
            except ValueError:
                pass

        except IndexError:
            # df_fix = df_fix.append({'Fixation': 0}, ignore_index=True).astype(int)
            pass
    df_fix = df_fix.shift(periods=1, axis=0, fill_value=1)
    # d = df['Fixation'] = df_fix
    # d['Fixation'] = d['Fixation'].notna().astype(int)
    return df_fix


# Generiert Geschwindigkeiten
# dx & dy = differenz. d = Abstand, vx & vy = Geschwindigkeit in x oder y Richtung [px/s],
# v = Betrag des Geschwindigkeitsvektor [px/s], a = Richtung
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

            try:
                dx = df.iloc[j]['Gaze X'] - df.iloc[i]['Gaze X']
            except ValueError:
                pass
            try:
                dy = df.iloc[j]['Gaze Y'] - df.iloc[i]['Gaze Y']
            except ValueError:
                pass

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
                {'dx': dx, 'dy': dy, 'd': d, 'vx': vx, 'vy': vy, 'v': v, 'a': a},
                ignore_index=True)
        except IndexError:
            pass
    return df_rad.astype(int)


# Generiert Sakkaden

def sac(df):
    df_sac = pd.DataFrame({'Saccades': [], 'Saccade Duration': [], 'Lost Track Dauer': []})
    # f = 0
    for i in range(len(df)):
        try:
            j = i + 1
            d = 120
            t = df.iloc[j]['Timestamp in ms'] - df.iloc[i]['Timestamp in ms']
            try:
                if df.iloc[i]['Fixation'] == 0 and df.iloc[i]['Lost Track'] == 0:
                    df_sac = df_sac.append({'Saccades': 1, 'Saccade Duration': t}, ignore_index=True).astype(int)
                    if np.isnan() == True:
                        pass
                else:
                    df_sac = df_sac.append({'Saccades': 0, 'Saccade Duration': 0}, ignore_index=True)
                    if df.iloc[j]['Fixation'] == 0 or (np.sqrt((df.iloc[i]['Gaze X'] - df.iloc[j]['Gaze X']) ** 2) >= d \
                                                       and np.sqrt(
                                (df.iloc[i]['Gaze Y'] - df.iloc[j]['Gaze Y']) ** 2) >= d):
                        # f += 1
                        if np.isnan() == True:
                            pass
                    else:
                        pass
            except ValueError:
                pass
        except IndexError:
            # df_fix = df_fix.append({'Fixation': 0}, ignore_index=True).astype(int)
            pass
    # df_fix = df_fix.shift(periods=1, axis=0, fill_value= 1)
    # d = df['Fixation'] = df_fix
    # d['Fixation'] = d['Fixation'].notna().astype(int)
    return df_sac


def lost_t(df):
    df_ltt = pd.DataFrame({'Lost Track Dauer': []})
    for i in range(len(df)):
        p = i - 1
        ltt = df.iloc[i]['Timestamp in ms'] - df.iloc[p]['Timestamp in ms']
        try:
            if df.iloc[i]['Lost Track'] == 1:
                df_ltt = df_ltt.append({'Lost Track Dauer': ltt}, ignore_index=True).astype(int)
            else:
                df_ltt = df_ltt.append({'Lost Track Dauer': 0}, ignore_index=True).astype(int)
        except IndexError:
            pass
    return df_ltt

def filter(df):

    return