from Funzioni_imputazione.riempi_Home_Planet import riempi_Home_Planet
from Funzioni_imputazione.riempi_VIP import riempi_VIP
from Funzioni_imputazione.riempi_cryo import riempi_cryo
from Funzioni_imputazione.riempi_cabin import riempi_cabin
from Funzioni_imputazione.riempi_Destination import riempi_Destination
from Funzioni_imputazione.riempi_Surname import riempi_Surname

def imputazione(df):
    df = riempi_Home_Planet(df)
    df = riempi_Surname(df)
    df= riempi_Destination(df)
    return df
