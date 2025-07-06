import pandas as pd

def riempi_side(combined_df):
    
    train_df1 = combined_df[combined_df['IsTrain'] == True].copy()
    val_df1 = combined_df[combined_df['IsTrain'] == False].copy()

    # === IMPUTAZIONE SIDE ===
    CS_bef = train_df1['Side'].isna().sum()

    # Gruppi con almeno 2 membri
    group_counts = train_df1['Group'].value_counts()
    gruppi_con_almeno_due = group_counts[group_counts >= 2].index

    # Calcola la Side più frequente per questi gruppi
    SCS_gb = (
        train_df1[train_df1['Group'].isin(gruppi_con_almeno_due)]
        .groupby(['Group', 'Side'])
        .size()
        .unstack(fill_value=0)
    )
    side_mode_per_group = SCS_gb.idxmax(axis=1)

    # Imputa Side per i gruppi con valore predominante
    side_nan_mask = train_df1['Side'].isna()
    group_with_mode_side = train_df1.loc[side_nan_mask, 'Group'].isin(side_mode_per_group.index)
    SCS_index = train_df1[side_nan_mask & group_with_mode_side].index
    train_df1.loc[SCS_index, 'Side'] = train_df1.loc[SCS_index, 'Group'].map(side_mode_per_group)

    # Imputa tutti i rimanenti valori mancanti in Side usando Transported
    train_df1.loc[train_df1['Side'].isna() & (train_df1['Transported'] == True), 'Side'] = 'S'
    train_df1.loc[train_df1['Side'].isna() & (train_df1['Transported'] == False), 'Side'] = 'P'

    CS_aft = train_df1['Side'].isna().sum()
    print(f"#Side missing values before: {CS_bef}")
    print(f"#Side missing values after:  {CS_aft}")

    side_mode = train_df1['Side'].mode()[0]
    # Riempie i NaN in Side nel validation set con la moda del train
    val_df1.loc[:, 'Side'] = val_df1['Side'].fillna(side_mode)


    # Unisce i due DataFrame
    combined_df= pd.concat([train_df1, val_df1], ignore_index=True)

    return combined_df