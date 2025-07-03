import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Percorso del file CSV
csv_file = 'C:/Users/dvita/Desktop/TITANIC/train.csv'

# Legge il file CSV
df = pd.read_csv(csv_file)

# Nuova feature - Group (presupponendo che 'PassengerId' sia nel formato '123_45')
df['Group'] = df['PassengerId'].apply(lambda x: x.split('_')[0]).astype(int)

# Nuova feature - Group size
group_counts = df['Group'].value_counts()
df['Group_size'] = df['Group'].map(group_counts)

palette = {True: 'green', False: 'red'}


# Pie plot con colori personalizzati
df['Transported'].value_counts().plot.pie(
    explode=[0.1, 0.1],
    autopct='%1.1f%%',
    shadow=True,
    textprops={'fontsize': 16},
    colors=[palette[False], palette[True]]
).set_title("Target distribution")

plt.ylabel('')  # Rimuove etichetta dell'asse y
plt.show()

# Figure size
plt.figure(figsize=(20,4))

# Histogram Group
sns.histplot(data=df, x='Group', hue='Transported', binwidth=1, kde=True, palette=palette)
plt.title('Group')
plt.xlabel('Group')
plt.ylabel('Numero di passeggeri')

plt.subplot(1,2,2)
sns.countplot(data=df, x='Group_size', hue='Transported', palette=palette)
plt.title('Group size')
plt.tight_layout()

# Nuova feature - Solo
df['Solo'] = (df['Group_size'] == 1).astype(int)

# Distribuzione della feature 'Solo'
plt.figure(figsize=(10,4))
sns.countplot(data=df, x='Solo', hue='Transported', palette=palette)
plt.title('Passenger travelling solo or not')
plt.ylim([0,3000])
plt.tight_layout()
plt.show()

# Estrae le componenti della Cabina
df[['Deck', 'CabinNum', 'Side']] = df['Cabin'].str.split('/', expand=True)
df['CabinNum'] = pd.to_numeric(df['CabinNum'], errors='coerce')

plt.figure(figsize=(10,6))
sns.histplot(data=df, x='CabinNum', hue='Transported', binwidth=20, palette=palette)
plt.vlines(300, ymin=0, ymax=200, color='black')
plt.vlines(600, ymin=0, ymax=200, color='black')
plt.vlines(900, ymin=0, ymax=200, color='black')
plt.vlines(1200, ymin=0, ymax=200, color='black')
plt.vlines(1500, ymin=0, ymax=200, color='black')
plt.vlines(1800, ymin=0, ymax=200, color='black')
plt.title('Cabin number')
plt.xlim([0, 2000])
plt.show()

# New features - training set
df['Cabin_region1'] = (df['CabinNum'] < 300).astype(int)  # one-hot encoding
df['Cabin_region2'] = ((df['CabinNum'] >= 300) & (df['CabinNum'] < 600)).astype(int)
df['Cabin_region3'] = ((df['CabinNum'] >= 600) & (df['CabinNum'] < 900)).astype(int)
df['Cabin_region4'] = ((df['CabinNum'] >= 900) & (df['CabinNum'] < 1200)).astype(int)
df['Cabin_region5'] = ((df['CabinNum'] >= 1200) & (df['CabinNum'] < 1500)).astype(int)
df['Cabin_region6'] = ((df['CabinNum'] >= 1500) & (df['CabinNum'] < 1800)).astype(int)
df['Cabin_region7'] = (df['CabinNum'] >= 1800).astype(int)

exp_feats = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']

fig, axes = plt.subplots(3, 2, figsize=(15, 15))
axes = axes.flatten()

for i, feat in enumerate(exp_feats):
    sns.histplot(data=df, x=feat, bins=30, kde=False, hue='Transported', palette=palette, ax=axes[i])
    # Rimuovo il titolo
    # axes[i].set_title(f'Distribuzione spese per {feat}')
    axes[i].set_xlabel(feat, labelpad=15)  # alza l’etichetta x
    axes[i].set_ylabel('Numero di passeggeri')

# Elimina eventuali subplot vuoti
if len(exp_feats) < len(axes):
    for j in range(len(exp_feats), len(axes)):
        fig.delaxes(axes[j])

plt.tight_layout()
plt.subplots_adjust(hspace=0.4)  # aumenta lo spazio verticale tra i plot
plt.show()



df['Expendures'] = df[['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']].sum(axis=1, skipna=True)

# Crea la colonna booleana: 1 se ha speso 0, 0 altrimenti
df['NoSpending'] = (df['Expendures'] == 0).astype(int)

# Calcolo della mediana
expendures_median = df['Expendures'].median()
print(expendures_median)

plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Expendures', bins=30, kde=False, hue='Transported', palette=palette)
plt.title('Distribuzione delle spese totali (Expendures)')
plt.xlabel('Expendures')
plt.ylabel('Numero di passeggeri')
plt.show()

# Filtro per Expendures < mediana
filtered_data = df[df['Expendures'] <= expendures_median]
x2 = df[df['Expendures'] > expendures_median]

# Conta quanti sono Transported = True e False
transported_counts1 = filtered_data['Transported'].value_counts()
transported_counts2 = x2['Transported'].value_counts()

# Stampa i conteggi
print("Conto di 'Transported' per passeggeri con Expendures < mediana:")
print(transported_counts1)
print("Conto di 'Transported' per passeggeri con Expendures > mediana:")
print(transported_counts2)

# Creazione della feature binaria
df['Expendures'] = (df['Expendures'] > expendures_median)

cat_feats = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP', 'Expendures', 'NoSpending']

# Prima figura con i primi 3 grafici
plt.figure(figsize=(10, 12))
for i, var_name in enumerate(cat_feats[:3]):
    ax = plt.subplot(3,1,i+1)
    sns.countplot(data=df, x=var_name, hue='Transported', palette=palette, ax=ax)
    ax.xaxis.labelpad = -5
    if i < 2:  # rimuove la legenda da tutti tranne l'ultimo
        ax.get_legend().remove()
plt.tight_layout()
plt.show()

# Seconda figura con gli ultimi 3 grafici
plt.figure(figsize=(10, 12))
for i, var_name in enumerate(cat_feats[3:]):
    ax = plt.subplot(3,1,i+1)
    sns.countplot(data=df, x=var_name, hue='Transported', palette=palette, ax=ax)
    ax.xaxis.labelpad = -5
    # Mostra legenda solo nel primo plot della seconda figura
    if i == 0:
        ax.legend(title='Transported')
    else:
        ax.get_legend().remove()
plt.tight_layout()
plt.show()


# Figure size
plt.figure(figsize=(10,4))

# Histogram
sns.histplot(data=df, x='Age', hue='Transported', binwidth=1, kde=True, palette=palette)

# Aesthetics
plt.title('Age distribution')
plt.xlabel('Age (years)')
plt.show()

# Calcola il numero di HomePlanet unici per gruppo
df_group_hp = df.groupby('Group')['HomePlanet'].nunique().reset_index(name='UniqueHomePlanets')

# Crea una nuova colonna testuale per plotting
df_group_hp['PlanetCount'] = df_group_hp['UniqueHomePlanets'].astype(str)

# Plot: countplot per il numero di pianeti unici nei gruppi
plt.figure(figsize=(10, 4))
ax = plt.subplot(1, 1, 1)
sns.countplot(data=df_group_hp, x='PlanetCount', ax=ax)

# Estetica
ax.set_xlabel('Numero di pianeti unici nel gruppo')
ax.set_ylabel('Numero di gruppi')
ax.set_title('Distribuzione del numero di HomePlanet per gruppo')
plt.tight_layout()
plt.show()

# Distribuzione deck e home planet
deck_hp=df.groupby(['Deck','HomePlanet'])['HomePlanet'].size().unstack().fillna(0)

# Heatmap di missing values
plt.figure(figsize=(10,4))
sns.heatmap(deck_hp.T, annot=True, fmt='g', cmap='coolwarm')
plt.figure(figsize=(6,6))

# Joint distribution of HomePlanet and Destination
hp_dest=df.groupby(['HomePlanet','Destination'])['Destination'].size().unstack().fillna(0)

# Heatmap of missing values
plt.figure(figsize=(10,4))
sns.heatmap(hp_dest.T, annot=True, fmt='g', cmap='coolwarm')
