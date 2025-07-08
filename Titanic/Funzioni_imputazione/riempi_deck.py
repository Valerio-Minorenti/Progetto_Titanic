from collections import Counter

def riempi_deck(combined_df):
    # === IMPUTAZIONE DECK ===
    CD_bef = combined_df['Deck'].isna().sum()

    train_df = combined_df[combined_df['IsTrain'] == True].copy()

    # Calcola la modalità del deck per ogni gruppo SOLO sul train
    GCD_gb = train_df.groupby(['Group', 'Deck']).size().unstack(fill_value=0)
    deck_mode_per_group = GCD_gb.idxmax(axis=1)

    # Maschera per missing Deck nel combined_df
    deck_nan_mask = combined_df['Deck'].isna()

    # Solo gruppi presenti in deck_mode_per_group (cioè con deck mode calcolato)
    group_with_mode = combined_df.loc[deck_nan_mask, 'Group'].isin(deck_mode_per_group.index)

    # Indici da imputare
    GCD_index = combined_df[deck_nan_mask & group_with_mode].index

    # Imputa Deck nei missing con la moda calcolata sul train
    combined_df.loc[GCD_index, 'Deck'] = combined_df.loc[GCD_index, 'Group'].map(deck_mode_per_group)
    
    # Riempie i missing con 'T'
    combined_df['Deck'].fillna('T', inplace=True)

    CD_aft = combined_df['Deck'].isna().sum()

    print(f"#Deck missing values before: {CD_bef}")
    print(f"#Deck missing values after:  {CD_aft}")

    return combined_df

