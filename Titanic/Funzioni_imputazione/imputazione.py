from Funzioni_imputazione.riempi_Home_Planet import riempi_Home_Planet

def imputazione(df):
    df = riempi_Home_Planet(df)
    df = riempi_Destination(df)
    df = riempi_Surname(df)
    return df
