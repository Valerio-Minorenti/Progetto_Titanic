import pandas as pd
from Funzioni_imputazione.converti_valori_e_colonne import converti_valori_colonne
from Funzioni_imputazione.imputazione import imputazione
# Percorsi dei file
csv_file = 'C:/Users/Standard/Desktop/Titanic/progetto_Soda/train.csv'
excel_file = 'C:/Users/Standard/Desktop/Titanic/progetto_Soda/trainozzo.xlsx'
output_file = 'tabellozza.xlsx'
# Prepara il dataset (conversioni + colonne pulite)
df = converti_valori_colonne(csv_file, excel_file, output_file)
#imputazione
df = imputazione(df)
# Salva il file finale aggiornato
df.to_excel(output_file, index=False)
print(f"Dataset finale salvato in: '{output_file}'")
