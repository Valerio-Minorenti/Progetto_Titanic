import pandas as pd

def encoding_dinamico(combined_df):
    """
    Applica One-Hot Encoding al dataset completo `combined_df`, 
    e salva i file codificati in percorsi forniti dinamicamente dall'utente.
    Restituisce train, val e test codificati separatamente.
    """

    print("\nColonne presenti nel dataset:")
    print(combined_df.columns)

    # === Percorsi output dinamici ===
    output_train = input("\nInserisci il percorso per salvare il TRAIN codificato (.xlsx): ")
    output_val   = input("Inserisci il percorso per salvare il VALIDATION codificato (.xlsx): ")
    output_test  = input("Inserisci il percorso per salvare il TEST codificato (.xlsx): ")

    # === Colonne da codificare ===
    cols_to_encode = ['HomePlanet', 'Deck', 'Side', 'Group_size']

    # One-Hot Encoding con drop_first=True per evitare multicollinearità
    df_encoded = pd.get_dummies(combined_df[cols_to_encode], drop_first=True)

    # Rimuovo le colonne originali codificate
    df_rest = combined_df.drop(columns=cols_to_encode)

    # Concateno le colonne codificate con il resto del DataFrame
    df_final = pd.concat([df_rest, df_encoded], axis=1)

    # === Estrai i dataset codificati ===
    df_train_encoded = df_final[df_final['IsTrain'] == True]
    df_val_encoded   = df_final[df_final['IsValidation'] == True]
    df_test_encoded  = df_final[df_final['IsTest'] == True]

    # === Salva i dataset ===
    df_train_encoded.to_excel(output_train, index=False)
    df_val_encoded.to_excel(output_val, index=False)
    df_test_encoded.to_excel(output_test, index=False)

    print("\nFile salvati correttamente:")
    print(f"   Train codificato -> {output_train}")
    print(f"   Val codificato   -> {output_val}")
    print(f"   Test codificato  -> {output_test}")

    return df_train_encoded, df_val_encoded, df_test_encoded

