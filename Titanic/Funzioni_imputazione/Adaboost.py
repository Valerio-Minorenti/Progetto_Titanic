import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

def run_adaboost_classification(path_to_csv, target_column, test_size=0.2, random_state=42):
    """
    Esegue classificazione AdaBoost con valutazione, inclusa la confusion matrix.

    Args:
        path_to_csv (str): percorso al file .csv contenente i dati.
        target_column (str): nome della colonna target (etichetta).
        test_size (float): percentuale del test set.
        random_state (int): seme casuale per riproducibilità.
    """

    # === Caricamento dati ===
    df = pd.read_csv(path_to_csv)

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # === Split train/test ===
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # === Modello AdaBoost ===
    base_model = DecisionTreeClassifier(max_depth=1)
    model = AdaBoostClassifier(
        base_estimator=base_model,
        n_estimators=100,
        learning_rate=1.0,
        random_state=random_state
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # === Valutazione ===
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {acc:.4f}\n")
    print("📋 Classification Report:\n", classification_report(y_test, y_pred))

    # === Confusion Matrix (numerica) ===
    cm = confusion_matrix(y_test, y_pred)
    print("📊 Confusion Matrix:\n", cm)

    # === Confusion Matrix (grafica) ===
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    disp.plot(cmap='Blues', values_format='d')
    plt.title("Confusion Matrix")
    plt.show()
