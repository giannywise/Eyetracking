"""
Export Ziel:
    Cliplänge
    Anzahl Fixationen - Done
    Gesamt Dauer Fixationen
    Anzahl Sakkaden - Done
    Gesamt Dauer Sakkaden - Done
    Anzahl Lost Tracks - Done
    Dauer Lost Tracks - Done
"""

del sys.modules['feature']
import pandas as pd
import feature as ft

df_filter = df_new[(df_new['Timestamp'].between(160,165) == True)]

### Cliplänge
 cl = input('Dauer des Clips:')

### Anzahl Lost tracks
df_filter['Lost Track'].sum()

### Dauer Lost Tracks
df_ltt = ft.lost_t(df_filter)
df_ltt['Lost Track Dauer'].sum()

### Anzahl an Saccaden
ft.sac(df_filter)
df_sacc = ft.sac(df_filter)
try:
    del df_filter['Saccades']
    del df_filter['level_0']
except KeyError:
    pass
df_filter = pd.concat([df_filter.reset_index(), df_sacc], axis=1, )
df_filter
df_filter['Saccades'].value_counts(sort=False)
sac_count = df_filter['Saccades'].value_counts(sort=False).filter(like='1')
sac_count

### Gesamt Dauer Sakkaden
df_sacc = ft.sac(df_filter)
try:
    del df_filter['Saccades']
    del df_filter['Saccade Duration']
    del df_filter['level_0']
except KeyError: pass
df_filter = pd.concat([df_filter.reset_index(),df_sacc],axis=1,)
df_filter['Saccade Duration'].sum()

### Anzahl Fixation
df_filter['Fixation'].loc[(df_filter['Fixation'] != 0)].tail(1).sum()

### Gesamt Dauer Fixation
 # Clip Länge - Gesamt Dauer Sakkaden + Gesamt Dauer Lost Tracks
