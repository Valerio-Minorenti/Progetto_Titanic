import pandas as pd

def riempi_vip(combined_df):
    # Separa i subset
    train_df = combined_df[combined_df['IsTrain'] == True].copy()
    val_df   = combined_df[combined_df['IsValidation'] == True].copy()
    test_df  = combined_df[combined_df['IsTest'] == True].copy()

    # === TRAIN ===
    before_train = train_df['VIP'].isna().sum()

    # Moda globale
    vip_mode_global = train_df['VIP'].mode().iloc[0]

    # Moda per gruppi con almeno 2 persone e VIP noto
    gruppi_vip_mode = (
        train_df[(train_df['Group_size'] >= 2) & train_df['VIP'].notna()]
        .groupby('Group')['VIP']
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else pd.NA)
        .to_dict()
    )

    # Imputazione per gruppo
    mask_group_train = train_df['VIP'].isna() & (train_df['Group_size'] >= 2) & train_df['Group'].isin(gruppi_vip_mode)
    train_df.loc[mask_group_train, 'VIP'] = train_df.loc[mask_group_train, 'Group'].map(gruppi_vip_mode)

    # Resto: moda globale
    train_df['VIP'] = train_df['VIP'].fillna(vip_mode_global)
    after_train = train_df['VIP'].isna().sum()
    print(f"[TRAIN] VIP mancanti prima: {before_train}, dopo: {after_train}")

    # === VALIDATION ===
    before_val = val_df['VIP'].isna().sum()
    mask_val = val_df['VIP'].isna() & (val_df['Group_size'] >= 2) & val_df['Group'].isin(gruppi_vip_mode)
    val_df.loc[mask_val, 'VIP'] = val_df.loc[mask_val, 'Group'].map(gruppi_vip_mode)
    val_df['VIP'] = val_df['VIP'].fillna(vip_mode_global)
    after_val = val_df['VIP'].isna().sum()
    print(f"[VAL] VIP mancanti prima: {before_val}, dopo: {after_val}")

    # === TEST ===
    before_test = test_df['VIP'].isna().sum()
    mask_test = test_df['VIP'].isna() & (test_df['Group_size'] >= 2) & test_df['Group'].isin(gruppi_vip_mode)
    test_df.loc[mask_test, 'VIP'] = test_df.loc[mask_test, 'Group'].map(gruppi_vip_mode)
    test_df['VIP'] = test_df['VIP'].fillna(vip_mode_global)
    after_test = test_df['VIP'].isna().sum()
    print(f"[TEST] VIP mancanti prima: {before_test}, dopo: {after_test}")

    # Ricombina
    combined_df = pd.concat([train_df, val_df, test_df], ignore_index=True)
    return combined_df
             