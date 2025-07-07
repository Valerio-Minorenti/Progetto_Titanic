from Funzioni_imputazione.converti_valori_e_colonne import converti_valori_colonne
from Funzioni_imputazione.imputazione import imputazione
from Funzioni_imputazione.hold import holdout_split

def main():
    # Percorso file input e output DAVIDE
    #excel_file = 'C:/Users/dvita/Desktop/TITANIC/train.xlsx'
    #output_train = 'C:/Users/dvita/Desktop/TITANIC/train_holdout.xlsx'
    #output_val = 'C:/Users/dvita/Desktop/TITANIC/val_holdout.xlsx'

        # Percorso file input e output VALERIO
    excel_file = 'C:/Users/Standard/Desktop/Titanic/Titanic/train.csv'
    output_train = 'C:/Users/Standard/Desktop/Titanic/Titanic/train_holdout.xlsx'
    output_val = 'C:/Users/Standard/Desktop/Titanic/Titanic/val_holdout.xlsx'

    # 1) Split train/val da file iniziale
    holdout_split(
        input_path=excel_file, train_path=output_train, val_path=output_val, test_size=0.2, stratify_col='Transported', random_state=42
    )

    # 2) Pulizia e conversione colonne, ritorna combined_df
    combined_df = converti_valori_colonne()

    # 3) Imputazione sul combined_df
    combined_df = imputazione(combined_df)

    # Puoi salvare df_finale oppure stampare info
    print("Imputazione completata.")

if __name__ == "__main__":
    main()
    print("Esecuzione completata con successo.")

