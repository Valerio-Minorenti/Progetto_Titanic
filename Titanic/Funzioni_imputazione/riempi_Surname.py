import pandas as pd

def riempi_Surname(df):
    # 1. Se manca la colonna Group o Surname, la crea
    if 'Group' not in df.columns:
        df['Group'] = df['PassengerId'].str.split('_').str[0].astype(int)

    if 'Surname' not in df.columns:
        df['Surname'] = df['Name'].str.split().str[-1]

    # Conta valori mancanti PRIMA
    mancanti_prima = df['Surname'].isna().sum()

    # === IMPUTAZIONE PER GRUPPO ===
    # Considera solo gruppi con più di una persona
    gruppi_multipli = df['Group'].value_counts()
    gruppi_validi = gruppi_multipli[gruppi_multipli > 1].index

    # Costruisce mappa: Group → Surname (se univoco)
    surname_gruppo = (
        df[df['Group'].isin(gruppi_validi)]
        .dropna(subset=['Surname'])
        .groupby('Group')['Surname']
        .agg(lambda x: x.mode()[0] if x.nunique() == 1 else None)
        .dropna()
        .to_dict()
    )

    # Applica l'imputazione
    df['Surname'] = df.apply(
        lambda row: surname_gruppo.get(row['Group'], None)
        if pd.isna(row['Surname']) else row['Surname'],
        axis=1
    )

    # Conta valori mancanti DOPO
    mancanti_dopo = df['Surname'].isna().sum()

    # Stampa risultato
    print(f"Valori mancanti in 'Surname' prima: {mancanti_prima}")
    print(f"Valori mancanti in 'Surname' dopo:  {mancanti_dopo}")

    return df
