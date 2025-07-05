from Funzioni_imputazione.converti_valori_e_colonne import converti_valori_colonne
from Funzioni_imputazione.imputazione import imputazione


csv_file = 'C:/Users/Standard/Desktop/Titanic/Titanic/train.csv'
output_file = 'C:/Users/Standard/Desktop/Titanic/Titanic/Funzioni_imputazione/tabellozza.xlsx'
excel_file = 'C:/Users/Standard/Desktop/Titanic/Titanic/Funzioni_imputazione/tabellozza.xlsx'
# Converte e prepara
df = converti_valori_colonne(csv_file, output_file,excel_file)

# Applica imputazioni
df = imputazione(df)

# Salva il file finale aggiornato
df.to_excel(output_file, index=False)
print(f"Dataset finale salvato in: '{output_file}'")
