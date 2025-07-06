import pandas as pd

def riempi_Home_Planet(combined_df):
    if 'Group' not in combined_df.columns:
        combined_df['Group'] = combined_df['PassengerId'].str.split('_').str[0].astype(int)

    if 'Surname' not in combined_df.columns:
        combined_df['Surname'] = combined_df['Name'].str.split().str[-1]

    # Conta valori mancanti PRIMA
    mancanti_prima = combined_df['HomePlanet'].isna().sum()

    # === 1. IMPUTAZIONE PER GRUPPO ===
    gruppi_multipli = combined_df['Group'].value_counts()
    gruppi_validi = gruppi_multipli[gruppi_multipli > 1].index

    homeplanet_gruppo = (
        combined_df[combined_df['Group'].isin(gruppi_validi)]
        .dropna(subset=['HomePlanet'])
        .groupby('Group')['HomePlanet']
        .agg(lambda x: x.mode()[0] if x.nunique() == 1 else None)
        .dropna()
        .to_dict()
    )

    combined_df['HomePlanet'] = combined_df.apply(
        lambda row: homeplanet_gruppo.get(row['Group'], None)
        if pd.isna(row['HomePlanet']) else row['HomePlanet'],
        axis=1
    )

    # === 2. IMPUTAZIONE PER DECK ===
    cond_deck = combined_df['HomePlanet'].isna()
    combined_df.loc[cond_deck & (combined_df['Deck'] == 'G'), 'HomePlanet'] = 'Earth'
    combined_df.loc[cond_deck & (combined_df['Deck'].isin(['A', 'B', 'C', 'T'])), 'HomePlanet'] = 'Europa'

    # === 3. IMPUTAZIONE PER COGNOME ===
    cond_surname = combined_df['HomePlanet'].isna()

    # Mappa del cognome → HomePlanet più frequente
    homeplanet_surname = (
        combined_df.dropna(subset=['HomePlanet'])
        .groupby('Surname')['HomePlanet']
        .agg(lambda x: x.mode()[0] if not x.mode().empty else None)
        .dropna()
        .to_dict()
    )

    combined_df['HomePlanet'] = combined_df.apply(
        lambda row: homeplanet_surname.get(row['Surname'], row['HomePlanet'])
        if pd.isna(row['HomePlanet']) else row['HomePlanet'],
        axis=1
    )

    # Conta valori mancanti DOPO
    mancanti_dopo = combined_df['HomePlanet'].isna().sum()

    print(f"Valori mancanti in 'HomePlanet' prima: {mancanti_prima}")
    print(f"Valori mancanti in 'HomePlanet' dopo:  {mancanti_dopo}")
    print(f"Valori HomePlanet riempiti: {mancanti_prima - mancanti_dopo}")

    return combined_df