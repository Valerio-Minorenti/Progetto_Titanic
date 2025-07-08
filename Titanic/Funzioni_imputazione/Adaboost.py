import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.tree import DecisionTreeClassifier

def run_adaboost_classification(path_to_csv, target_column, test_size=0.2, random_state=42):
    """
    Esegue classificazione AdaBoost su un dataset CSV.

    Args:
        path_to_csv (str): percorso al file .csv contenente i dati.
        target_column (str): nome della colonna target (etichetta).
        test_size (float): percentuale del test set (default 0.2).
        random_state (int): seme casuale per riproducibilità.
    """

    # === Carica dati ===
    df = pd.read_csv(path_to_csv)

    # === Separa X e y ===
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # === Split train/test ===
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # === Crea il modello AdaBoost ===
    base_model = DecisionTreeClassifier(max_depth=1)
    model = AdaBoostClassifier(base_estimator=base_model, n_estimators=100, learning_rate=1.0, random_state=random_state)

    # === Allena il modello ===
    model.fit(X_train, y_train)

    # === Predizione ===
    y_pred = model.predict(X_test)

    # === Valutazione ===
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {acc:.4f}")
    print("\n📋 Classification Report:\n", classification_report(y_test, y_pred))
