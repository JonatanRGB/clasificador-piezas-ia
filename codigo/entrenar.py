"""
Semana 7: entrena el clasificador, lo evalua y guarda modelo.pkl
Uso (desde la raiz del repo):  python codigo/entrenar.py
"""
import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

features = pd.read_csv('datos/features.csv')
X = features.drop(columns=['ventana', 'etiqueta'])   # ventana es un identificador: meterla seria fuga de datos
y = features['etiqueta']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    stratify=y,
    random_state=42,
)
print(f"Entrenamiento: {len(X_train)} ventanas | Prueba: {len(X_test)} ventanas")

escalador = StandardScaler()
X_train_esc = escalador.fit_transform(X_train)
X_test_esc = escalador.transform(X_test)      # transform, NO fit_transform

candidatos = {
    'kNN (k=5)': KNeighborsClassifier(n_neighbors=5),
    'Arbol (max_depth=3)': DecisionTreeClassifier(max_depth=3, random_state=42),
}

print(f"\n{'Modelo':<22}{'Exact. entrenamiento':>22}{'Exact. prueba':>16}")
for nombre, m in candidatos.items():
    m.fit(X_train_esc, y_train)
    tr = accuracy_score(y_train, m.predict(X_train_esc))
    te = accuracy_score(y_test, m.predict(X_test_esc))
    print(f"{nombre:<22}{tr:>22.3f}{te:>16.3f}")

# Me quedo con el arbol: mejor exactitud en prueba que kNN y se puede leer (son 3 preguntas).
ELEGIDO = 'Arbol (max_depth=3)'
modelo = candidatos[ELEGIDO]
print("\nReglas que aprendio el arbol:")
print(export_text(modelo, feature_names=list(X.columns)))
y_pred = modelo.predict(X_test_esc)
print(f"\nModelo elegido: {ELEGIDO}")
print("Exactitud:", accuracy_score(y_test, y_pred))
print("Matriz de confusion:")
etiquetas = sorted(y.unique())
print(etiquetas)
print(confusion_matrix(y_test, y_pred, labels=etiquetas))

joblib.dump({'modelo': modelo, 'escalador': escalador, 'columnas': list(X.columns)},
            'modelo.pkl')
print("Guardado modelo.pkl (modelo + escalador + columnas)")

os.makedirs('figuras', exist_ok=True)
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, labels=etiquetas, cmap='Blues')
plt.title(f'Matriz de confusion - {ELEGIDO} (prueba)')
plt.tight_layout()
plt.savefig('figuras/confusion.png', dpi=150)
print("Figura: figuras/confusion.png")
