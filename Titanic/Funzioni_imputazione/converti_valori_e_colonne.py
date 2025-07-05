import pandas as pd

def converti_valori_colonne(csv_file, excel_file, output_file):
    # Percorso del file CSV
    csv_file = 'C:/Users/dvita/Desktop/TITANIC/train.csv'

    # Percorso intermedio Excel
    excel_file = 'C:/Users/dvita/Desktop/TITANIC/train.xlsx'

    # Percorso finale
    output_file = 'tabellozza.xlsx'

    # Legge il file CSV
    df = pd.read_csv(csv_file)

    # Salva il file in formato Excel
    df.to_excel(excel_file, index=False)
    print(f"Conversione completata: '{csv_file}' → '{excel_file}'")

    # Riapre il file Excel
    df = pd.read_excel(excel_file)

    # Estrae il gruppo da PassengerId
    df['Group'] = df['PassengerId'].str.split('_').str[0].astype(int)

    # Nuova feature - Group size
    group_counts = df['Group'].value_counts()
    df['Group_size'] = df['Group'].map(group_counts)

    # Estrae le componenti della Cabina
    df[['Deck', 'CabinNum', 'Side']] = df['Cabin'].str.split('/', expand=True)

    # Droppa la colonna Cabin
    df.drop(columns=['Cabin'], inplace=True)

    # Estrae il cognome dalla colonna Name
    df['Surname'] = df['Name'].str.split().str[-1]

    # Droppa la colonna Name
    df.drop(columns=['Name'], inplace=True)

    # Riempie NaN con 0 per le spese
    spesa_cols = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    df[spesa_cols] = df[spesa_cols].fillna(0)

    # Calcola la spesa totale
    df['Expendures'] = df[spesa_cols].sum(axis=1)

    # Calcolo della mediana
    expendures_median = df['Expendures'].median()

    # Creazione della feature binaria
    df['Expendures'] = (df['Expendures'] > expendures_median)

    #Drop colonne spese
    df.drop(columns=spesa_cols, inplace=True)

    df.drop(columns=['Age'], inplace=True)

    # Salva il file finale
    df.to_excel(output_file, index=False)
    print(f"File finale salvato in: '{output_file}'")
    return df