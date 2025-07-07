import pandas as pd

def riempi_side(combined_df):
    # Separa i blocchi
    train_df = combined_df[combined_df['IsTrain'] == True].copy()
    val_df   = combined_df[combined_df['IsValidation'] == True].copy()
    test_df  = combined_df[combined_df['IsTest'] == True].copy()

    # --- Imputazione TRAIN ---
    CS_bef = train_df['Side'].isna().sum()

    # Imputa Side in base a Transported
    train_df.loc[train_df['Side'].isna() & (train_df['Transported'] == True), 'Side'] = 'S'
    train_df.loc[train_df['Side'].isna() & (train_df['Transported'] == False), 'Side'] = 'P'

    CS_aft = train_df['Side'].isna().sum()
    print(f"[TRAIN] Side missing values: prima = {CS_bef}, dopo = {CS_aft}")

    # --- Imputazione VAL e TEST ---
    side_mode = train_df['Side'].mode()[0]

    val_missing_before = val_df['Side'].isna().sum()
    val_df['Side'] = val_df['Side'].fillna(side_mode)
    val_missing_after = val_df['Side'].isna().sum()
    print(f"[VAL] Side missing: prima = {val_missing_before}, dopo = {val_missing_after}")

    test_missing_before = test_df['Side'].isna().sum()
    test_df['Side'] = test_df['Side'].fillna(side_mode)
    test_missing_after = test_df['Side'].isna().sum()
    print(f"[TEST] Side missing: prima = {test_missing_before}, dopo = {test_missing_after}")

    # --- Ricombina tutto ---
    combined_df = pd.concat([train_df, val_df, test_df], ignore_index=True)
    return combined_df