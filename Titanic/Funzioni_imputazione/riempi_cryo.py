import pandas as pd

def riempi_cryo(df):
    # Conta valori mancanti PRIMA
    cryo_nan_before = df['CryoSleep'].isna().sum()
    expend_nan_before = df['Expendures'].isna().sum()

    # 1. Riempie CryoSleep usando NoSpending
    df.loc[df['CryoSleep'].isna() & (df['NoSpending'] == 1), 'CryoSleep'] = True
    df.loc[df['CryoSleep'].isna() & (df['NoSpending'] == 0), 'CryoSleep'] = False

    # Conta valori mancanti DOPO
    cryo_nan_after = df['CryoSleep'].isna().sum()

    # Stampa il risultato
    print(f"CryoSleep - Valori mancanti prima: {cryo_nan_before}, dopo: {cryo_nan_after}")

    return df