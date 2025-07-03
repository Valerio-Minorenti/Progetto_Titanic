import pandas as pd

def converti_valori_colonne(csv_file, output_file):
    # Legge il CSV originale
    df = pd.read_csv(csv_file)

    # Estrai il gruppo da PassengerId
    df['Group'] = df['PassengerId'].str.split('_').str[0].astype(int)

    # Estrai le componenti della Cabina
    df[['Deck', 'Num', 'Side']] = df['Cabin'].str.split('/', expand=True)

    # Droppa la colonna Cabin
    df.drop(columns=['Cabin'], inplace=True)

    # Estrai il cognome dalla colonna Name
    df['Surname'] = df['Name'].str.split().str[-1]

    # Droppa la colonna Name
    df.drop(columns=['Name'], inplace=True)

    # Riempie NaN con 0 per le spese
    spesa_cols = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    df[spesa_cols] = df[spesa_cols].fillna(0)

    # Calcola la spesa totale
    df['Expendures'] = df[spesa_cols].sum(axis=1)

    # Crea la colonna booleana: 1 se ha speso 0, 0 altrimenti
    df['NoSpending'] = (df['Expendures'] == 0).astype(int)

    # Calcolo della mediana
    expendures_median = df['Expendures'].median()

    # Creazione della feature binaria
    df['Expendures'] = (df['Expendures'] > expendures_median)

    #Drop colonne spese
    df.drop(columns=spesa_cols, inplace=True)

    # 7. Crea AgeGroup con pd.cut
    df['AgeGroup'] = pd.cut(
        df['Age'],
        bins=[-1, 18, 25, float('inf')],
        labels=['0-18', '19-25', '25+']
    ).astype(str)

    df.loc[df['Age'].isna(), 'AgeGroup'] = 'NaN'

    df.drop(columns=['Age'], inplace=True)

    # Salva il file Excel finale
    df.to_excel(output_file, index=False)
    print(f"File Excel finale salvato in: '{output_file}'")

    return df
