from Funzioni_imputazione.riempi_Home_Planet import riempi_Home_Planet
from Funzioni_imputazione.riempi_VIP import riempi_VIP
from Funzioni_imputazione.riempi_cryo import riempi_cryo
from Funzioni_imputazione.riempi_cabin import riempi_cabin
from Funzioni_imputazione.riempi_Destination import riempi_Destination
from Funzioni_imputazione.riempi_Surname import riempi_Surname
from Funzioni_imputazione.riempi_side import riempi_side

def imputazione(combined_df):
    combined_df = riempi_Home_Planet(combined_df)
    combined_df = riempi_VIP(combined_df)
    combined_df = riempi_cryo(combined_df)
    combined_df = riempi_cabin(combined_df)
    combined_df = riempi_side(combined_df)
    combined_df = riempi_Surname(combined_df)
    combined_df = riempi_Destination(combined_df)
    return combined_df