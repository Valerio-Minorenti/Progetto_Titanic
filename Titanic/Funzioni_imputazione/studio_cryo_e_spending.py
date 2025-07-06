# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 11:17:57 2025

@author: matmi
"""
import pandas as pd

# 1. Caricamento dataset
df = pd.read_csv("C:/Users/matmi/Desktop/Progetto_titanic_versionato/Titanic/train.csv")

# 2. Lista delle colonne di spesa
spending_cols = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']

# 3. Riempie i NaN con 0 per sommare correttamente
df[spending_cols] = df[spending_cols].fillna(0)

# 4. Crea la colonna booleana 'Spending'
df['Spending'] = df[spending_cols].sum(axis=1) > 0

# 5. Analisi: relazione tra CryoSleep e Spending
cryosleep_true_spending_true = df[(df['CryoSleep'] == True) & (df['Spending'] == True)]
cryosleep_true_spending_false = df[(df['CryoSleep'] == True) & (df['Spending'] == False)]
cryosleep_false_spending_true = df[(df['CryoSleep'] == False) & (df['Spending'] == True)]
cryosleep_false_spending_false = df[(df['CryoSleep'] == False) & (df['Spending'] == False)]

# 6. Stampa i risultati
print("CryoSleep == True & Spending == True:", cryosleep_true_spending_true.shape[0])
print("CryoSleep == True & Spending == False:", cryosleep_true_spending_false.shape[0])
print("CryoSleep == False & Spending == True:", cryosleep_false_spending_true.shape[0])
print("CryoSleep == False & Spending == False:", cryosleep_false_spending_false.shape[0])

# 7. Percentuale di CryoSleep con spese
cryosleep_true = df[df['CryoSleep'] == True]
if not cryosleep_true.empty:
    perc_spesa_in_cryo = (cryosleep_true_spending_true.shape[0] / cryosleep_true.shape[0]) * 100
    print(f"Percentuale di persone in CryoSleep che hanno speso: {perc_spesa_in_cryo:.2f}%")
