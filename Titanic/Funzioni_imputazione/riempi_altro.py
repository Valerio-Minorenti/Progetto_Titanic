import pandas as pd

def riempi_cryo(combined_df):
    # Conta valori mancanti PRIMA
    cryo_nan_before = combined_df['CryoSleep'].isna().sum()

    # 1. Riempie CryoSleep usando NoSpending
    combined_df.loc[combined_df['CryoSleep'].isna() & (combined_df['NoSpending'] == 1), 'CryoSleep'] = True
    combined_df.loc[combined_df['CryoSleep'].isna() & (combined_df['NoSpending'] == 0), 'CryoSleep'] = False

    # Conta valori mancanti DOPO
    cryo_nan_after = combined_df['CryoSleep'].isna().sum()

    # Stampa il risultato
    print(f"CryoSleep - Valori mancanti prima: {cryo_nan_before}, dopo: {cryo_nan_after}")

    return combined_df