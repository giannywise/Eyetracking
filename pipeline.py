"""
Export Ziel:
    Cliplänge
    Anzahl Fixationen - Done
    Gesamt Dauer Fixationen Done
    Anzahl Sakkaden - Done
    Gesamt Dauer Sakkaden - Done
    Anzahl Lost Tracks - Done
    Dauer Lost Tracks - Done
"""
import sys
#del sys.modules['feature']
import pandas as pd
import feature as ft
import sys
import os


def feat(s, e):
    f_name = 'features/feature' + '_' + str(s) + '-' + str(e)

    if os.path.exists(f_name + ".csv"):
        os.remove(f_name + ".csv")
        print("The file has been deleted successfully")
    else:
        print("The file does not exist!")

    directory = 'Daten/'

    df_final = pd.DataFrame({'Szene': [],'Cliplänge in Sekunden': [], 'Anzahl Sakkaden': [], 'Gesamt Dauer Sakkaden': [],
                             "Anzahl Lost Tracks": [], "Dauer Lost Tracks": [], "Anzahl Fixationen": [],
                             "Gesamt Dauer Fixationen": []})
    name = pd.DataFrame({'Name': []})

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f) and not filename.startswith('.'):
            df = pd.read_csv(f, sep=",")
            df = ft.pipe(df, s, e)
            name = name.append({'Name': filename}, ignore_index=True)
            df_final = pd.concat([df_final,df], ignore_index=True)
            print(df_final)
            print(filename)

    df_final = pd.concat([df_final, name], axis=1)
    print(df_final)
    df_final.to_csv('features/feature' + '_' + str(s) + '-' + str(e) + ".csv")



#feat().to_csv('feature.csv')