import pandas as pd

def converti_valori_colonne():

    # === 1. Carica i file ===
    train_df = pd.read_excel('C:/Users/dvita/Desktop/TITANIC/train_holdout.xlsx')
    val_df   = pd.read_excel('C:/Users/dvita/Desktop/TITANIC/val_holdout.xlsx')
    test_df  = pd.read_csv('C:/Users/dvita/Desktop/TITANIC/test.csv')

    # === 2. Aggiungi flag identificativi ===
    train_df['IsTrain'] = True
    train_df['IsValidation'] = False
    train_df['IsTest'] = False

    val_df['IsTrain'] = False
    val_df['IsValidation'] = True
    val_df['IsTest'] = False

    test_df['IsTrain'] = False
    test_df['IsValidation'] = False
    test_df['IsTest'] = True

    # === 3. Unisci i tre dataset ===
    combined_df = pd.concat([train_df, val_df, test_df], ignore_index=True)

    # === 4. Feature Engineering ===

    # Group
    combined_df['Group'] = combined_df['PassengerId'].str.split('_').str[0].astype(int)

    # Group size solo su train
    group_counts = combined_df['Group'].value_counts()
    combined_df['Group_size'] = combined_df['Group'].map(group_counts)

    # Split Cabin
    combined_df[['Deck', 'CabinNum', 'Side']] = combined_df['Cabin'].str.split('/', expand=True)
    combined_df.drop(columns=['Cabin'], inplace=True)

    # Surname
    combined_df['Surname'] = combined_df['Name'].str.split().str[-1]
    combined_df.drop(columns=['Name'], inplace=True)

    # Calcolo spese
    spesa_cols = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    combined_df[spesa_cols] = combined_df[spesa_cols].fillna(0)
    combined_df['Expendures'] = combined_df[spesa_cols].sum(axis=1)

    # Flag per chi non ha speso nulla
    combined_df['NoSpending'] = combined_df['Expendures'] == 0

    # Calcola la mediana solo sul training
    expendures_median = combined_df.loc[combined_df['IsTrain'], 'Expendures'].median()

    # Binarizza expendures
    combined_df['Expendures'] = combined_df['Expendures'] > expendures_median

    # Drop colonne originali spese + Age se presente
    combined_df.drop(columns=spesa_cols, inplace=True)
    if 'Age' in combined_df.columns:
        combined_df.drop(columns=['Age'], inplace=True)

    # === 5. Ritaglia i dataset finali ===
    new_train = combined_df[combined_df['IsTrain']== True].copy()
    new_val   = combined_df[combined_df['IsValidation']== True].copy()
    new_test  = combined_df[combined_df['IsTest']== True].copy()

    # === 6. Salva i file finali ===
    new_train.to_excel('C:/Users/dvita/Desktop/TITANIC/train_df.xlsx', index=False)
    new_val.to_excel('C:/Users/dvita/Desktop/TITANIC/val_df.xlsx', index=False)
    new_test.to_excel('C:/Users/dvita/Desktop/TITANIC/test_df.xlsx', index=False)

    print("File salvati correttamente.")
    return combined_df

