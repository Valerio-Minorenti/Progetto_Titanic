import pandas as pd

def missing_values(combined_df):
    """
    1. Calcola i valori mancanti per colonna (escludendo 'Transported')
    2. Calcola quante righe hanno almeno un valore mancante (dopo il drop delle colonne inutili)
    3. Droppa colonne inutili
    4. Droppa righe con valori mancanti
    5. Suddivide il DataFrame nei 3 subset (train, val, test)
    6. Salva i file
    """


    # === 1. Calcolo missing per colonna (escludendo 'Transported') ===
    df_check_before_drop = combined_df.drop(columns=['Transported'], errors='ignore')
    missing_per_column = df_check_before_drop.isna().sum()
    missing_per_column = missing_per_column[missing_per_column > 0]

    print("Valori mancanti per colonna (prima del drop, escluso 'Transported'):\n")
    if missing_per_column.empty:
        print("Nessun valore mancante trovato.")
    else:
        print(missing_per_column.sort_values(ascending=False))
        print(f"\nTotale valori mancanti nel DataFrame: {missing_per_column.sum()}")

    # === 2. Drop colonne inutili ===
    columns_to_drop = [
        'Group', 'Destination', 'VIP', 'Surname', 'CabinNum',
        'NoSpending', 'PassengerId'
    ]
    combined_df = combined_df.drop(columns=columns_to_drop, errors='ignore')

    # === 3. Calcolo righe con almeno un valore mancante (dopo il drop) ===
    df_check_after_drop = combined_df.drop(columns=['Transported'], errors='ignore')
    num_campioni_con_missing = df_check_after_drop.isna().any(axis=1).sum()
    percentuale = num_campioni_con_missing / len(df_check_after_drop) * 100

    print(f"\nNumero di campioni con almeno un valore mancante (dopo il drop colonne): {num_campioni_con_missing}")
    print(f"Percentuale rispetto al totale: {percentuale:.2f}%")


# 4. Drop righe con valori mancanti solo su train + val
    mask_trainval = combined_df['IsTrain'] | combined_df['IsValidation']
    combined_df = pd.concat([
        combined_df[mask_trainval].dropna(),
        combined_df[~mask_trainval]  # test rimane com'è
    ])

    return combined_df
