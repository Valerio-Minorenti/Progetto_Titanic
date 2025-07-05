import pandas as pd
from sklearn.model_selection import StratifiedKFold

def kfold_cross_validation(
    input_path='C:/Users/Standard/Desktop/Titanic/Titanic/train.csv',
    output_dir='C:/Users/Standard/Desktop/Titanic/Titanic/kfold.xlsx',
    n_splits=5,
    save=True
):
    df = pd.read_csv(input_path)
    df['kfold'] = -1

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Crea i fold
    for fold, (_, val_idx) in enumerate(skf.split(df, df['Transported'])):
        df.loc[val_idx, 'kfold'] = fold

    # Per ogni fold: separa e salva (opzionale)
    for fold in range(n_splits):
        train_df = df[df['kfold'] != fold].copy().reset_index(drop=True)
        val_df = df[df['kfold'] == fold].copy().reset_index(drop=True)

        print(f"\n🔁 Fold {fold}")
        print(f"Train: {train_df.shape[0]} righe")
        print(f"Validation: {val_df.shape[0]} righe")

        if save:
            train_path = f'{output_dir}train_fold{fold}.xlsx'
            val_path = f'{output_dir}val_fold{fold}.xlsx'
            train_df.to_excel(train_path, index=False)
            val_df.to_excel(val_path, index=False)
            print(f"✅ Salvati: {train_path}, {val_path}")

    return df

# Esegui la funzione
df_with_folds = kfold_cross_validation()
