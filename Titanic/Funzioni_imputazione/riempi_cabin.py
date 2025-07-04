from collections import Counter
import pandas as pd

def riempi_cabin(df):
    # === IMPUTAZIONE DECK ===
    CD_bef = df['Deck'].isna().sum()

    # Calcola il deck più frequente per ogni gruppo
    GCD_gb = df.groupby(['Group', 'Deck']).size().unstack(fill_value=0)
    deck_mode_per_group = GCD_gb.idxmax(axis=1)

    # Imputa Deck per i gruppi con valore predominante
    deck_nan_mask = df['Deck'].isna()
    group_with_mode = df.loc[deck_nan_mask, 'Group'].isin(deck_mode_per_group.index)
    GCD_index = df[deck_nan_mask & group_with_mode].index
    df.loc[GCD_index, 'Deck'] = df.loc[GCD_index, 'Group'].map(deck_mode_per_group)

    # Imputa i rimanenti NaN con il Deck meno usato (bilanciamento)
    deck_counts = Counter(df['Deck'].dropna())
    for idx in df[df['Deck'].isna()].index:
        min_count = min(deck_counts.values(), default=0)
        least_used_decks = [deck for deck, count in deck_counts.items() if count == min_count]
        chosen_deck = least_used_decks[0]
        df.at[idx, 'Deck'] = chosen_deck
        deck_counts[chosen_deck] += 1

    CD_aft = df['Deck'].isna().sum()
    print(f"#Deck missing values before: {CD_bef}")
    print(f"#Deck missing values after:  {CD_aft}")

    # === IMPUTAZIONE SIDE ===
    CS_bef = df['Side'].isna().sum()

    # Gruppi con almeno 2 membri
    group_counts = df['Group'].value_counts()
    gruppi_con_almeno_due = group_counts[group_counts >= 2].index

    # Calcola la Side più frequente per questi gruppi
    SCS_gb = (
        df[df['Group'].isin(gruppi_con_almeno_due)]
        .groupby(['Group', 'Side'])
        .size()
        .unstack(fill_value=0)
    )
    side_mode_per_group = SCS_gb.idxmax(axis=1)

    # Imputa Side per i gruppi con valore predominante
    side_nan_mask = df['Side'].isna()
    group_with_mode_side = df.loc[side_nan_mask, 'Group'].isin(side_mode_per_group.index)
    SCS_index = df[side_nan_mask & group_with_mode_side].index
    df.loc[SCS_index, 'Side'] = df.loc[SCS_index, 'Group'].map(side_mode_per_group)

    # Imputa tutti i rimanenti valori mancanti in Side usando Transported
    df.loc[df['Side'].isna() & (df['Transported'] == True), 'Side'] = 'S'
    df.loc[df['Side'].isna() & (df['Transported'] == False), 'Side'] = 'P'

    CS_aft = df['Side'].isna().sum()
    print(f"#Side missing values before: {CS_bef}")
    print(f"#Side missing values after:  {CS_aft}")

    return df