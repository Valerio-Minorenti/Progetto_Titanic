import pandas as pd

def encoding_statico(combined_df):
    """
    Applica One-Hot Encoding al dataset completo `combined_df` 
    (contenente le colonne booleane: is_train, is_val, is_test),
    e restituisce train, val e test codificati separatamente.

    Salva anche i tre dataset codificati in formato CSV.
    """

    # === Percorsi output ===
    #output_train = 'C:/Users/Standard/Desktop/Titanic/Titanic/train_encoded.csv'
    #output_val = 'C:/Users/Standard/Desktop/Titanic/Titanic/val_encoded.csv'
    #output_test = 'C:/Users/Standard/Desktop/Titanic/Titanic/test_encoded.csv'

    output_train = 'C:/Users/dvita/Desktop/TITANIC/train_encoded.xlsx'
    output_val = 'C:/Users/dvita/Desktop/TITANIC/val_encoded.xlsx'
    output_test = 'C:/Users/dvita/Desktop/TITANIC/test_encoded.xlsx'

    # Colonne da codificare
    cols_to_encode = ['HomePlanet', 'Deck', 'Side', 'Group_size']

    # One-Hot Encoding solo su queste colonne, con drop_first=True per evitare multicollinearità
    df_encoded = pd.get_dummies(combined_df[cols_to_encode], drop_first=True)

    # Rimuovo le colonne originali codificate
    df_rest = combined_df.drop(columns=cols_to_encode)

    # Concateno le colonne codificate con il resto del DataFrame
    df_final = pd.concat([df_rest, df_encoded], axis=1)

    # === Estrai i dataset codificati ===
    df_train_encoded = df_final[df_final['IsTrain'] == True].drop(columns=['IsTrain', 'IsValidation', 'IsTest'])
    df_val_encoded = df_final[df_final['IsValidation'] == True].drop(columns=['IsTrain', 'IsValidation', 'IsTest'])
    df_test_encoded = df_final[df_final['IsTest'] == True].drop(columns=['IsTrain', 'IsValidation', 'IsTest'])

    # === Salva i dataset in CSV ===
    df_train_encoded.to_excel(output_train, index=False)
    df_val_encoded.to_excel(output_val, index=False)
    df_test_encoded.to_excel(output_test, index=False)

    print(f"Train codificato salvato in: {output_train}")
    print(f"Val codificato salvato in:   {output_val}")
    print(f"Test codificato salvato in:  {output_test}")

    return df_train_encoded, df_val_encoded, df_test_encoded

