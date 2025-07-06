from collections import Counter

def riempi_deck(combined_df):
    # === IMPUTAZIONE DECK ===
    CD_bef = combined_df['Deck'].isna().sum()

    # Calcola il deck più frequente per ogni gruppo
    GCD_gb = combined_df.groupby(['Group', 'Deck']).size().unstack(fill_value=0)
    deck_mode_per_group = GCD_gb.idxmax(axis=1)

    # Imputa Deck per i gruppi con valore predominante
    deck_nan_mask = combined_df['Deck'].isna()
    group_with_mode = combined_df.loc[deck_nan_mask, 'Group'].isin(deck_mode_per_group.index)
    GCD_index = combined_df[deck_nan_mask & group_with_mode].index
    combined_df.loc[GCD_index, 'Deck'] = combined_df.loc[GCD_index, 'Group'].map(deck_mode_per_group)

    # Imputa i rimanenti NaN con il Deck meno usato (bilanciamento)
    deck_counts = Counter(combined_df['Deck'].dropna())
    for idx in combined_df[combined_df['Deck'].isna()].index:
        min_count = min(deck_counts.values(), default=0)
        least_used_decks = [deck for deck, count in deck_counts.items() if count == min_count]
        chosen_deck = least_used_decks[0]
        combined_df.at[idx, 'Deck'] = chosen_deck
        deck_counts[chosen_deck] += 1

    CD_aft = combined_df['Deck'].isna().sum()
    print(f"#Deck missing values before: {CD_bef}")
    print(f"#Deck missing values after:  {CD_aft}")

    return combined_df

