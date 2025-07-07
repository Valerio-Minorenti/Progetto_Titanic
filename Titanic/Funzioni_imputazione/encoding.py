import pandas as pd

def encoding_statico(df=None):
    """
    Applica One-Hot Encoding su train e validation,
    garantendo coerenza, e salva i risultati in formato CSV.
    Se df è passato, restituisce la parte di train codificata.
    """

    # === Percorsi input/output ===
    input_train = 'C:/Users/Standard/Desktop/Titanic/Titanic/train_holdout.xlsx'
    input_val = 'C:/Users/Standard/Desktop/Titanic/Titanic/val_holdout.xlsx'
    output_train = 'C:/Users/Standard/Desktop/Titanic/Titanic/train_encoded.csv'
    output_val = 'C:/Users/Standard/Desktop/Titanic/Titanic/val_encoded.csv'

    # === Carica i dataset ===
    df_train = pd.read_excel(input_train)
    df_val = pd.read_excel(input_val)

    # === Etichette per unione temporanea ===
    df_train['__is_train'] = True
    df_val['__is_train'] = False

    # === Combina e codifica ===
    df_combined = pd.concat([df_train, df_val], axis=0)
    df_encoded = pd.get_dummies(df_combined, drop_first=True)

    # === Split codificato ===
    df_train_encoded = df_encoded[df_encoded['__is_train'] == True].drop(columns='__is_train')
    df_val_encoded = df_encoded[df_encoded['__is_train'] == False].drop(columns='__is_train')

    # === Salva i file codificati in CSV ===
    df_train_encoded.to_csv(output_train, index=False)
    df_val_encoded.to_csv(output_val, index=False)

    print(f"✅ Train codificato salvato in: {output_train}")
    print(f"✅ Val codificato salvato in:   {output_val}")

    # Restituisce il DataFrame solo se serve in catena
    if df is not None:
        return df_train_encoded
