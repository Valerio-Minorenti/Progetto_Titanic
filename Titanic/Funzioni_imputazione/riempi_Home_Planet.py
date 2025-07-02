import pandas as pd

def riempi_Home_Planet(df):
    if 'Group' not in df.columns:
        df['Group'] = df['PassengerId'].str.split('_').str[0].astype(int)

    if 'Surname' not in df.columns:
        df['Surname'] = df['Name'].str.split().str[-1]

    # Conta valori mancanti PRIMA
    mancanti_prima = df['HomePlanet'].isna().sum()

    # === 1. IMPUTAZIONE PER GRUPPO ===
    gruppi_multipli = df['Group'].value_counts()
    gruppi_validi = gruppi_multipli[gruppi_multipli > 1].index

    homeplanet_gruppo = (
        df[df['Group'].isin(gruppi_validi)]
        .dropna(subset=['HomePlanet'])
        .groupby('Group')['HomePlanet']
        .agg(lambda x: x.mode()[0] if x.nunique() == 1 else None)
        .dropna()
        .to_dict()
    )

    df['HomePlanet'] = df.apply(
        lambda row: homeplanet_gruppo.get(row['Group'], None)
        if pd.isna(row['HomePlanet']) else row['HomePlanet'],
        axis=1
    )

    # === 2. IMPUTAZIONE PER DECK ===
    cond_deck = df['HomePlanet'].isna()
    df.loc[cond_deck & (df['Deck'] == 'G'), 'HomePlanet'] = 'Earth'
    df.loc[cond_deck & (df['Deck'].isin(['A', 'B', 'C', 'T'])), 'HomePlanet'] = 'Europa'

    # === 3. IMPUTAZIONE PER COGNOME ===
    cond_surname = df['HomePlanet'].isna()

    # Mappa del cognome → HomePlanet più frequente
    homeplanet_surname = (
        df.dropna(subset=['HomePlanet'])
        .groupby('Surname')['HomePlanet']
        .agg(lambda x: x.mode()[0] if not x.mode().empty else None)
        .dropna()
        .to_dict()
    )

    df['HomePlanet'] = df.apply(
        lambda row: homeplanet_surname.get(row['Surname'], row['HomePlanet'])
        if pd.isna(row['HomePlanet']) else row['HomePlanet'],
        axis=1
    )

    # Conta valori mancanti DOPO
    mancanti_dopo = df['HomePlanet'].isna().sum()

    print(f"Valori mancanti in 'HomePlanet' prima: {mancanti_prima}")
    print(f"Valori mancanti in 'HomePlanet' dopo:  {mancanti_dopo}")

    return df
