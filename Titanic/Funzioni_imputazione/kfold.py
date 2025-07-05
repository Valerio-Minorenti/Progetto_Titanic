import pandas as pd
from sklearn.model_selection import StratifiedKFold

def kfold(df, save=False, output_train='C:/Users/dvita/Desktop/TITANIC/train_split.xlsx', output_val='C:/Users/dvita/Desktop/TITANIC/val_split.xlsx'):
    """
    Divide il dataset in train e validation usando StratifiedKFold sul target 'Transported'.
    
    Args:
        path_csv (str): percorso del file CSV originale (es. 'train.csv')
        save (bool): se True salva i file su disco
        output_train (str): nome file Excel per il train
        output_val (str): nome file Excel per il validation

    Returns:
        train_df, val_df (DataFrame, DataFrame)
    """
    df = pd.read_csv('C:/Users/dvita/Desktop/TITANIC/train.csv')

    # StratifiedKFold
    df['kfold'] = -1
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for fold, (_, val_idx) in enumerate(skf.split(df, df['Transported'])):
        df.loc[val_idx, 'kfold'] = fold
        break  # usa solo fold 0

    # Crea i DataFrame
    train_df = df[df['kfold'] != 0].copy().reset_index(drop=True)
    val_df = df[df['kfold'] == 0].copy().reset_index(drop=True)

    train_df.drop(columns='kfold', inplace=True)
    val_df.drop(columns='kfold', inplace=True)

    # Salva su file (opzionale)
    if save:
        train_df.to_excel(output_train, index=False)
        val_df.to_excel(output_val, index=False)
        print(f"File salvati")

    return train_df, val_df