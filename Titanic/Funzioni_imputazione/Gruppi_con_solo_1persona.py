# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 15:11:29 2025

@author: matmi
"""
import pandas as pd
import matplotlib.pyplot as plt

# Caricamento del dataset
df = pd.read_csv("C:/Users/Standard/Desktop/Titanic/Titanic/train.csv")

# Estrazione del gruppo dal PassengerId
df['Group'] = df['PassengerId'].str.split('_').str[0]

# Conta le dimensioni dei gruppi
group_sizes = df.groupby('Group').size()

# Conta quanti gruppi hanno 1 sola persona e quanti ne hanno >= 2
solo_count = (group_sizes == 1).sum()
group_count = (group_sizes >= 2).sum()

# Dizionario dei conteggi
group_counts = {
    'Gruppi con 1 persona': solo_count,
    'Gruppi con >= 2 persone': group_count
}

# Creazione del grafico a barre
plt.figure(figsize=(6, 4))
plt.bar(group_counts.keys(), group_counts.values(), color='skyblue')
plt.ylabel("Numero di gruppi")
plt.title("Distribuzione gruppi per dimensione")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()



