import pandas as pd

def riempi_Destination(df):
    # Conta valori mancanti PRIMA
    mancanti_prima = df['Destination'].isna().sum()

    # === 1. IMPUTAZIONE PER COGNOME ===
    cond_surname = df['Destination'].isna()

    # Mappa cognome → Destination più frequente
    destination_surname = (
        df.dropna(subset=['Destination'])
        .groupby('Surname')['Destination']
        .agg(lambda x: x.mode()[0] if not x.mode().empty else None)
        .dropna()
        .to_dict()
    )

    df['Destination'] = df.apply(
        lambda row: destination_surname.get(row['Surname'], row['Destination'])
        if pd.isna(row['Destination']) else row['Destination'],
        axis=1
    )

    # === 2. IMPUTAZIONE PER HomePlanet = Mars ===
    cond_mars = (df['Destination'].isna()) & (df['HomePlanet'] == 'Mars')
    df.loc[cond_mars, 'Destination'] = 'TRAPPIST-1e'

    # === 3. IMPUTAZIONE PER HomePlanet = Earth ===
    cond_earth = (df['Destination'].isna()) & (df['HomePlanet'] == 'Earth')
    df.loc[cond_earth, 'Destination'] = 'TRAPPIST-1e'

    # Conta valori mancanti DOPO
    mancanti_dopo = df['Destination'].isna().sum()

    # Stampa risultati
    print(f"Valori mancanti in 'Destination' prima: {mancanti_prima}")
    print(f"Valori mancanti in 'Destination' dopo:  {mancanti_dopo}")
    print(f"Valori Destination riempiti: {mancanti_prima - mancanti_dopo}")

    return df
