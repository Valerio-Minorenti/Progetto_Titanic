import pandas as pd

def converti_valori_colonne(csv_file, excel_file, output_file):
    # Legge il file CSV
    df = pd.read_csv(csv_file)

    # Salva il file in formato Excel intermedio
    df.to_excel(excel_file, index=False)
    print(f"Conversione completata: '{csv_file}' → '{excel_file}'")

    # Riapre il file Excel
    df = pd.read_excel(excel_file)

    # Estrae il gruppo da PassengerId
    df['Group'] = df['PassengerId'].str.split('_').str[0].astype(int)

    # Estrae le componenti della Cabina
    df[['Deck', 'Num', 'Side']] = df['Cabin'].str.split('/', expand=True)

    # Droppa la colonna Cabin
    df.drop(columns=['Cabin'], inplace=True)

    # Estrae il cognome dalla colonna Name
    df['Surname'] = df['Name'].str.split().str[-1]

    # Droppa la colonna Name
    df.drop(columns=['Name'], inplace=True)

    # Salva il file finale
    df.to_excel(output_file, index=False)
    print(f"File finale salvato in: '{output_file}'")

    return df
