import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === INPUT DINAMICO FILE ===
path_excel = input("Inserisci il percorso del file .xlsx da caricare: ")
df = pd.read_excel(path_excel)

# === FEATURE ENGINEERING ===
df['Group'] = df['PassengerId'].apply(lambda x: x.split('_')[0]).astype(int)
group_counts = df['Group'].value_counts()
df['Group_size'] = df['Group'].map(group_counts)
df['Surname'] = df['Name'].str.split().str[-1]

palette = {True: 'green', False: 'red'}

# === PIE PLOT ===
df['Transported'].value_counts().plot.pie(
    explode=[0.1, 0.1],
    autopct='%1.1f%%',
    shadow=True,
    textprops={'fontsize': 16},
    colors=[palette[False], palette[True]]
).set_title("Target distribution")

plt.ylabel('')
plt.show()

# === GROUP & GROUP SIZE PLOTS ===
plt.figure(figsize=(20,4))
sns.histplot(data=df, x='Group', hue='Transported', binwidth=1, kde=True, palette=palette)
plt.title('Group')
plt.xlabel('Group')
plt.ylabel('Numero di passeggeri')

plt.subplot(1,2,2)
sns.countplot(data=df, x='Group_size', hue='Transported', palette=palette)
plt.title('Group size')
plt.tight_layout()
plt.show()

# === CABIN COMPONENTS ===
df[['Deck', 'CabinNum', 'Side']] = df['Cabin'].str.split('/', expand=True)
df['CabinNum'] = pd.to_numeric(df['CabinNum'], errors='coerce')

plt.figure(figsize=(10,6))
sns.histplot(data=df, x='CabinNum', hue='Transported', binwidth=20, palette=palette)
for x in range(300, 2001, 300):
    plt.vlines(x, ymin=0, ymax=200, color='black')
plt.title('Cabin number')
plt.xlim([0, 2000])
plt.show()

# === CABIN REGION FEATURES ===
df['Cabin_region1'] = (df['CabinNum'] < 300).astype(int)
df['Cabin_region2'] = ((df['CabinNum'] >= 300) & (df['CabinNum'] < 600)).astype(int)
df['Cabin_region3'] = ((df['CabinNum'] >= 600) & (df['CabinNum'] < 900)).astype(int)
df['Cabin_region4'] = ((df['CabinNum'] >= 900) & (df['CabinNum'] < 1200)).astype(int)
df['Cabin_region5'] = ((df['CabinNum'] >= 1200) & (df['CabinNum'] < 1500)).astype(int)
df['Cabin_region6'] = ((df['CabinNum'] >= 1500) & (df['CabinNum'] < 1800)).astype(int)
df['Cabin_region7'] = (df['CabinNum'] >= 1800).astype(int)

# === EXPENDITURE FEATURES ===
exp_feats = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']

fig, axes = plt.subplots(3, 2, figsize=(15, 15))
axes = axes.flatten()
for i, feat in enumerate(exp_feats):
    sns.histplot(data=df, x=feat, bins=30, kde=False, hue='Transported', palette=palette, ax=axes[i])
    axes[i].set_xlabel(feat, labelpad=15)
    axes[i].set_ylabel('Numero di passeggeri')

if len(exp_feats) < len(axes):
    for j in range(len(exp_feats), len(axes)):
        fig.delaxes(axes[j])

plt.tight_layout()
plt.subplots_adjust(hspace=0.4)
plt.show()

# === EXPENDITURE TOTALE + BINARIA ===
df['Expendures'] = df[exp_feats].sum(axis=1, skipna=True)
expendures_median = df['Expendures'].median()
print(f"Mediana Expendures: {expendures_median}")

plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Expendures', bins=30, kde=False, hue='Transported', palette=palette)
plt.title('Distribuzione delle spese totali (Expendures)')
plt.xlabel('Expendures')
plt.ylabel('Numero di passeggeri')
plt.show()

filtered_data = df[df['Expendures'] <= expendures_median]
x2 = df[df['Expendures'] > expendures_median]
print("Conto di 'Transported' per Expendures <= mediana:")
print(filtered_data['Transported'].value_counts())
print("Conto di 'Transported' per Expendures > mediana:")
print(x2['Transported'].value_counts())

# === CRYOSLEEP ANALISI ===
cryo_false = df[df['CryoSleep'] == False]
mediana_expendures = cryo_false['Expendures'].median()
print(f"Mediana Expendures per CryoSleep=False: {mediana_expendures}")
df['Expendures'] = (df['Expendures'] > expendures_median)

# === GRAFICI CATEGORICI ===
cat_feats = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP', 'Expendures']

plt.figure(figsize=(10, 12))
for i, var_name in enumerate(cat_feats[:3]):
    ax = plt.subplot(3,1,i+1)
    sns.countplot(data=df, x=var_name, hue='Transported', palette=palette, ax=ax)
    ax.xaxis.labelpad = -5
    if i < 2:
        ax.get_legend().remove()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 12))
for i, var_name in enumerate(cat_feats[3:]):
    ax = plt.subplot(3,1,i+1)
    sns.countplot(data=df, x=var_name, hue='Transported', palette=palette, ax=ax)
    ax.xaxis.labelpad = -5
    if i == 0:
        ax.legend(title='Transported')
    else:
        ax.get_legend().remove()
plt.tight_layout()
plt.show()

# === AGE DISTRIBUTION ===
plt.figure(figsize=(10,4))
sns.histplot(data=df, x='Age', hue='Transported', binwidth=1, kde=True, palette=palette)
plt.title('Age distribution')
plt.xlabel('Age (years)')
plt.show()

# === GRUPPI & HOMEPLANET ===
df_group_hp = df.groupby('Group')['HomePlanet'].nunique().reset_index(name='UniqueHomePlanets')
df_group_hp['PlanetCount'] = df_group_hp['UniqueHomePlanets'].astype(str)

plt.figure(figsize=(10, 4))
ax = plt.subplot(1, 1, 1)
sns.countplot(data=df_group_hp, x='PlanetCount', ax=ax)
ax.set_xlabel('Numero di pianeti unici nel gruppo')
ax.set_ylabel('Numero di gruppi')
ax.set_title('Distribuzione del numero di HomePlanet per gruppo')
plt.tight_layout()
plt.show()

# === HEATMAPS ===
deck_hp = df.groupby(['Deck','HomePlanet'])['HomePlanet'].size().unstack().fillna(0)
plt.figure(figsize=(10,4))
sns.heatmap(deck_hp.T, annot=True, fmt='g', cmap='coolwarm')
plt.show()

hp_dest = df.groupby(['HomePlanet','Destination'])['Destination'].size().unstack().fillna(0)
plt.figure(figsize=(10,4))
sns.heatmap(hp_dest.T, annot=True, fmt='g', cmap='coolwarm')
plt.show()

# === UNIQUE SURNAME ===
surname_counts = df['Surname'].value_counts()
df['UniqueSurname'] = df['Surname'].map(lambda x: 1 if pd.notna(x) and surname_counts[x] == 1 else 0)

plt.figure(figsize=(6, 5))
sns.countplot(data=df, x='UniqueSurname', hue='Transported', palette=palette)
plt.title('Distribuzione di Transported rispetto a unicità del cognome')
plt.xlabel('Cognome Unico (1 = sì, 0 = no)')
plt.ylabel('Conteggio')
plt.xticks([0, 1], ['Condiviso', 'Unico'])
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# === VIP COERENZA NEI GRUPPI ===
group_sizes = df['Group'].value_counts()
gruppi_validi = group_sizes[group_sizes >= 2].index
df_valid = df[df['Group'].isin(gruppi_validi) & df['VIP'].notna()].copy()

def percentuale_vip_uguali(gruppo):
    mode = gruppo['VIP'].mode()
    if mode.empty:
        return None
    return (gruppo['VIP'] == mode.iloc[0]).mean()

percentuali = df_valid.groupby('Group').apply(percentuale_vip_uguali)
media_percentuali_vip = round(percentuali.mean() * 100, 2)
print(f"Percentuale media di VIP coerenti nei gruppi: {media_percentuali_vip}%")

# === CRYOSLEEP + SPESA ===
cryosleep_true = df[df['CryoSleep'] == True]
num_zero_expendures = (cryosleep_true['Expendures'] == 0).sum()
total_cryosleep = len(cryosleep_true)
percentuale = num_zero_expendures / total_cryosleep * 100
print(f"Percentuale di passeggeri con Expendures = 0 tra CryoSleep=True: {percentuale:.2f}%")
