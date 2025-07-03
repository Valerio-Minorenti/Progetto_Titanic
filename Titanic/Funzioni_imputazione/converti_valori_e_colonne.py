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

    # Salva il file Excel finale
    df.to_excel(output_file, index=False)
    print(f"File Excel finale salvato in: '{output_file}'")

    return df
