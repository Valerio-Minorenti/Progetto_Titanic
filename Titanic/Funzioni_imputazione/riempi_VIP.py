import pandas as pd

def riempi_VIP(df):


    missing_vip_before = df['VIP'].isna().sum()
    percent_vip_before = round(missing_vip_before / len(df) * 100, 2)
    print(f"[PRIMA] Valori mancanti in 'VIP': {missing_vip_before} ({percent_vip_before}%)")
    # Estrai il gruppo
    df['Group'] = df['PassengerId'].str.split('_').str[0]

    # Conta dimensione dei gruppi
    group_sizes = df['Group'].value_counts()
    gruppi_validi = group_sizes[group_sizes >= 2].index

    # Filtra solo gruppi con almeno 2 persone e VIP noto
    df_filtrato = df[df['Group'].isin(gruppi_validi) & df['VIP'].notna()].copy()

    # Calcola la moda di VIP per ciascun gruppo (solo tra quelli validi)
    group_vip_mode = (
        df_filtrato.groupby('Group')['VIP']
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else pd.NA)
        .to_dict()
    )

    # Imputazione per gruppo (solo dove VIP è NaN)
    vip_nan_mask = df['VIP'].isna() & df['Group'].isin(group_vip_mode)
    df.loc[vip_nan_mask, 'VIP'] = df.loc[vip_nan_mask, 'Group'].map(group_vip_mode)

    # Fallback globale: usa la moda globale per i rimanenti
    if df['VIP'].isna().any():
        vip_mode_global = df['VIP'].mode().iloc[0]
        df['VIP'] = df['VIP'].fillna(vip_mode_global)

    # --- Qui va la tua imputazione, ad esempio:
    # df = imputazione(df)

    # === DOPO L’IMPUTAZIONE ===
    missing_vip_after = df['VIP'].isna().sum()
    percent_vip_after = round(missing_vip_after / len(df) * 100, 2)
    print(f"[DOPO]  Valori mancanti in 'VIP': {missing_vip_after} ({percent_vip_after}%)")
    return df
