from Funzioni_imputazione.riempi_Home_Planet import riempi_Home_Planet
from Funzioni_imputazione.riempi_VIP import riempi_vip
from Funzioni_imputazione.riempi_cryo import riempi_cryo
from Funzioni_imputazione.riempi_deck import riempi_deck
from Funzioni_imputazione.riempi_Destination import riempi_Destination
from Funzioni_imputazione.riempi_Surname import riempi_Surname
from Funzioni_imputazione.riempi_side import riempi_side
from Funzioni_imputazione.missing_values import missing_values
from Funzioni_imputazione.encoding import encoding_statico
from Funzioni_imputazione.adaboost import adaboost

def imputazione(combined_df, target_column='Transported'):
    combined_df = riempi_Home_Planet(combined_df)
    combined_df = riempi_vip(combined_df)
    combined_df = riempi_cryo(combined_df)
    combined_df = riempi_deck(combined_df)
    combined_df = riempi_side(combined_df)
    combined_df = riempi_Surname(combined_df)
    combined_df = riempi_Destination(combined_df)
    combined_df = missing_values(combined_df)
    df_train_encoded, df_val_encoded, df_test_encoded = encoding_statico(combined_df)
    adaboost(df_train_encoded, df_val_encoded, target_column='Transported', n_estimators=100)


    
    return combined_df