import pandas as pd

def missing_values(combined_df):
    """
    1. Calcola i valori mancanti per colonna (escludendo 'Transported')
    2. Calcola quante righe hanno almeno un valore mancante (dopo il drop delle colonne inutili)
    3. Suddivide il DataFrame nei 3 subset (train, val, test)
    4. Droppa colonne inutili
    5. Salva i file
    """

    # === 1. Calcolo missing per colonna (escludendo 'Transported') ===
    df_check_before_drop = combined_df.drop(columns=['Transported'], errors='ignore')
    missing_per_column = df_check_before_drop.isna().sum()
    missing_per_column = missing_per_column[missing_per_column > 0]

    print("📋 Valori mancanti per colonna (prima del drop, escluso 'Transported'):\n")
    if missing_per_column.empty:
        print("✅ Nessun valore mancante trovato.")
    else:
        print(missing_per_column.sort_values(ascending=False))
        print(f"\n🧮 Totale valori mancanti nel DataFrame: {missing_per_column.sum()}")

    # === 2. Suddivisione nei 3 subset ===
    train_df = combined_df[combined_df['IsTrain'] == True].copy()
    val_df   = combined_df[combined_df['IsValidation'] == True].copy()
    test_df  = combined_df[combined_df['IsTest'] == True].copy()

    # === 3. Drop colonne inutili ===
    columns_to_drop = [
        'Group', 'Destination', 'VIP', 'Surname', 'CabinNum',
        'NoSpending', 'IsTrain', 'IsValidation', 'IsTest'
    ]

    for df in [train_df, val_df, test_df]:
        df.drop(columns=columns_to_drop, errors='ignore', inplace=True)

    # === 4. Calcolo righe con almeno un valore mancante (dopo il drop) ===
    combined_no_set = pd.concat([train_df, val_df, test_df], ignore_index=True)
    df_check_after_drop = combined_no_set.drop(columns=['Transported'], errors='ignore')
    num_campioni_con_missing = df_check_after_drop.isna().any(axis=1).sum()
    percentuale = num_campioni_con_missing / len(df_check_after_drop) * 100

    print(f"\n🔍 Numero di campioni con almeno un valore mancante (dopo il drop): {num_campioni_con_missing}")
    print(f"📊 Percentuale rispetto al totale: {percentuale:.2f}%")

    # === 5. Drop campioni con valori mancanti ===
    combined_no_set = combined_no_set.dropna()


    # === 5. Salvataggio ===
    train_df.to_excel('C:/Users/dvita/Desktop/TITANIC/train_imputed.xlsx', index=False)
    val_df.to_excel('C:/Users/dvita/Desktop/TITANIC/val_imputed.xlsx', index=False)
    test_df.to_excel('C:/Users/dvita/Desktop/TITANIC/test_imputed.xlsx', index=False)

    print("✅ File salvati con successo.")

    return train_df, val_df, test_df
