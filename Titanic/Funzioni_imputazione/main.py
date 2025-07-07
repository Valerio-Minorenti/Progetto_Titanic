from Funzioni_imputazione.converti_valori_e_colonne import converti_valori_colonne
from Funzioni_imputazione.imputazione import imputazione
from hold import holdout_split

def main():

    # 1) Split train/val da file iniziale
    holdout_split()

    # 2) Pulizia e conversione colonne, ritorna combined_df
    combined_df = converti_valori_colonne()

    # 3) Imputazione sul combined_df
    combined_df = imputazione(combined_df)

    # Puoi salvare df_finale oppure stampare info
    print("Imputazione completata.")

if __name__ == "__main__":
    main()
    print("Esecuzione completata con successo.")

