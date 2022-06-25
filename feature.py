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
    df_rad = pd.DataFrame({'dx': [], 'dy': [], 'd': [], 'vx': [], 'vy': [], 'v': [], 'a': []})
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
    return df_rad


# Generiert Sakkaden

def sac(df):
    df_sac = pd.DataFrame({'Saccades': [], 'Saccade Duration': []})
    # f = 0
    for i in range(len(df)):
        try:
            j = i + 1
            d = 100
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

# Generiert gesamt Dauer Lost Tracks
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

# Filtert den DataFrame
def filter(df, s, e):
    df = df[(df['Timestamp'].between(s, e) == True)].reset_index()
    try:
        df.drop(['level_0'], axis=1)
    except KeyError:
        pass
    df['Gaze Y'] = df['Gaze Y'].fillna(0)
    df['Gaze X'] = df['Gaze X'].fillna(0)
    df['Gaze X'] = df['Gaze X'].astype(int)
    df['Gaze Y'] = df['Gaze Y'].astype(int)
    df['Lost Track'] = df['Lost Track'].notna().astype(int)
    # Zeit in MS
    df['Timestamp in ms'] = df['Timestamp'] * 1000
    df['Timestamp in ms'] = df['Timestamp in ms'].astype(int)

    # Generiert Geschwindigkeit
    df_ges = ges(df)
    df = pd.concat([df, df_ges], axis=1)

    ### Filter
    # and (df_new["dy"] > 0) == True and df_new["dx"] <= 10 == True and df_new["dx"] >= -10 == True
    # df_new['dx'] = np.sqrt(df_new['dx'] ** 2)
    # df_new = df_new.loc[(df_new["dx"] >= 10) & (df_new["dx"] >= -10) == True]
    # df_new = df_new.loc[(df_new["dy"] >= 20 * df_new["dx"]) & (df_new["dy"] > 0) == False]
    # df_new = df_new.loc[(df_new["vx"] < -10) & (df_new["vx"] > 10) == False]
    # df_new = df_new.loc[(df_new["vy"] <= 2500) & (df_new['vx'] >= 100) == True]
    df = df[(df["Gaze Y"] <= 1030) == True]
    try:
        df.drop(['level_0'], axis=1)
    except KeyError:
        pass
    df['Fixation'] = fix(df)
    df = df.loc[(df['v'] == 0) & (df['Fixation'] == 0) == False]
    try:
        df.drop(['level_0'], axis=1)
    except KeyError:
        pass
    df

    # Sakkaden
    df_sacc = sac(df)
    df = pd.concat([df.reset_index(), df_sacc], axis=1, )

    # Lost Track Dauer
    df_ltt = lost_t(df)
    df = pd.concat([df, df_ltt], axis=1, )
    df.drop(df.tail(1).index, inplace=True)
    return df.drop(['level_0'], axis=1)


# Generiert die Features
def pipe(df, s, e):
    """
    df: Dataframe
    s: Start des Videos
    e: Ende des Videos
    """

    df = filter(df, s, e)

    ### Cliplänge
    clip = e - s

    ### Anzahl Lost tracks
    lt_count = df['Lost Track'].sum()

    ### Dauer Lost Tracks
    df_ltt = lost_t(df)
    ltt = df_ltt['Lost Track Dauer'].sum()

    ### Anzahl an Saccaden
    df['Saccades'].value_counts(sort=False)
    sac_count = df['Saccades'].value_counts(sort=False).filter(like='1').sum()

    ### Gesamt Dauer Sakkaden
    sacc_dur = df['Saccade Duration'].sum()

    ### Anzahl Fixation
    df_fix_count = df['Fixation'].max()

    ### Dauer_Fixation
    fix_dur = clip - (sacc_dur/1000 + ltt/1000)

    df_final = pd.DataFrame({'Cliplänge in Sekunden': clip, 'Anzahl Sakkaden': [], 'Gesamt Dauer Sakkaden': [],
                             "Anzahl Lost Tracks": [], "Dauer Lost Tracks": [], "Anzahl Fixationen": [],
                             "Gesamt Dauer Fixationen": []})

    df_final = df_final.append(
        {'Cliplänge in Sekunden': e - s, 'Anzahl Sakkaden': sac_count, 'Gesamt Dauer Sakkaden': sacc_dur,
         "Anzahl Lost Tracks": lt_count, "Dauer Lost Tracks": ltt, "Anzahl Fixationen": df_fix_count,
         "Gesamt Dauer Fixationen": fix_dur}, ignore_index=True)

    return df_final
