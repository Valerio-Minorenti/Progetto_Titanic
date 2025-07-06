
def riempi_cryo(combined_df):
    # Conta valori mancanti PRIMA
    cryo_nan_before = combined_df['CryoSleep'].isna().sum()

    # Converte CryoSleep in tipo boolean Pandas (nullable)
    if combined_df['CryoSleep'].dtype != 'boolean':
        combined_df['CryoSleep'] = combined_df['CryoSleep'].astype('boolean')

    # 1. Riempie CryoSleep usando Expendures == 0
    combined_df.loc[combined_df['CryoSleep'].isna() & (combined_df['Expendures'] == 0), 'CryoSleep'] = True
    combined_df.loc[combined_df['CryoSleep'].isna() & (combined_df['Expendures'] > 0), 'CryoSleep'] = False

    # Conta valori mancanti DOPO
    cryo_nan_after = combined_df['CryoSleep'].isna().sum()

    # Stampa il risultato
    print(f"CryoSleep - Valori mancanti prima: {cryo_nan_before}, dopo: {cryo_nan_after}")

    return combined_df
