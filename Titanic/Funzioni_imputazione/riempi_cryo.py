
def riempi_cryo(df):
    # Conta valori mancanti PRIMA
    cryo_nan_before = df['CryoSleep'].isna().sum()

    # Converte CryoSleep in tipo boolean Pandas (nullable)
    if df['CryoSleep'].dtype != 'boolean':
        df['CryoSleep'] = df['CryoSleep'].astype('boolean')

    # 1. Riempie CryoSleep usando Expendures == 0
    df.loc[df['CryoSleep'].isna() & (df['Expendures'] == 0), 'CryoSleep'] = True
    df.loc[df['CryoSleep'].isna() & (df['Expendures'] > 0), 'CryoSleep'] = False

    # Conta valori mancanti DOPO
    cryo_nan_after = df['CryoSleep'].isna().sum()

    # Stampa il risultato
    print(f"CryoSleep - Valori mancanti prima: {cryo_nan_before}, dopo: {cryo_nan_after}")

    return df
