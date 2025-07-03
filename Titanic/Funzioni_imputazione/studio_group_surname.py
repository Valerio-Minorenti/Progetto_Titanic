# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 14:51:57 2025

@author: matmi
"""
import pandas as pd

# Caricamento del dataset
df = pd.read_csv("C:/Users/Standard/Desktop/Titanic/Titanic/train.csv")  # metti il tuo path

# Estrai Group dal PassengerId
df['Group'] = df['PassengerId'].str.split('_').str[0]

# Estrai il cognome dall'ultima parola del nome
df['Surname'] = df['Name'].str.split().str[-1]

# Calcola quanti cognomi distinti ci sono in ogni gruppo
group_surname_counts = df.groupby('Group')['Surname'].nunique()

# Conta i gruppi coerenti (solo 1 cognome)
coherent_groups = (group_surname_counts == 1).sum()

# Totale gruppi
total_groups = group_surname_counts.shape[0]

# Percentuale gruppi coerenti
coherent_percentage = coherent_groups / total_groups * 100

# Righe con Surname mancante
missing_surnames = df['Surname'].isna().sum()

# Stampa dei risultati
print("Verifica se Group → Surname è affidabile")
print(f"Gruppi totali: {total_groups}")
print(f"Gruppi con 1 solo cognome: {coherent_groups}")
print(f"Percentuale di gruppi coerenti: {coherent_percentage:.2f}%")
print(f"Righe con Surname mancante: {missing_surnames}")


