import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

def cramers_v(confusion_matrix):
    chi2 = chi2_contingency(confusion_matrix, correction=False)[0]
    n = confusion_matrix.sum().sum()
    k = confusion_matrix.shape[0]
    r = confusion_matrix.shape[1]
    return np.sqrt(chi2 / (n * (min(k - 1, r - 1))))

# Carica il dataset
df = pd.read_excel("C:/Users/Standard/Desktop/Titanic/Titanic/Funzioni_imputazione/tabellozza.xlsx")  # o trainozzo.xlsx

# Prepara le variabili
df_valid = df.dropna(subset=['HomePlanet', 'Transported'])
df_valid['Transported'] = df_valid['Transported'].astype(str)

# Contingency table: cognome × trasportato
cont_tab = pd.crosstab(df_valid['HomePlanet'], df_valid['Transported'])

# Chi-quadro
chi2, pval, dof, expected = chi2_contingency(cont_tab)

# Cramér's V
cramer_v = cramers_v(cont_tab)

print("=== Risultati statistici ===")
print(f"Chi2 statistic: {chi2:.2f}")
print(f"p-value: {pval:.3g} (sotto 0.05 indica relazione significativa)")
print(f"Cramér's V: {cramer_v:.3f} (→ 0 nessuna relazione, verso 1 relazione forte)")
