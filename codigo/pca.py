# pca.py - reduce las caracteristicas a dos componentes y las grafica (semana 10)
# Uso (desde la raiz del repo):  python codigo/pca.py
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

features = pd.read_csv('datos/features.csv')

X = features.drop(columns=['ventana', 'etiqueta'])
y = features['etiqueta']          # NO se usa para calcular el PCA, solo para colorear

escalador = StandardScaler().fit(X)
X_esc = escalador.transform(X)

pca = PCA(n_components=2)
componentes = pca.fit_transform(X_esc)

print("Caracteristicas:", list(X.columns))
print("Varianza explicada por cada componente:", np.round(pca.explained_variance_ratio_, 3))
print("Varianza acumulada de las dos:", round(pca.explained_variance_ratio_.sum(), 3))
print("Peso de cada caracteristica en PC1 y PC2:")
print(pd.DataFrame(pca.components_.T, index=X.columns, columns=['PC1', 'PC2']).round(2))

# Puntos mas lejos del centro de su clase (posibles atipicos)
comp = pd.DataFrame(componentes, columns=['PC1', 'PC2'])
comp['ventana'] = features['ventana']
comp['etiqueta'] = y
centro = comp.groupby('etiqueta')[['PC1', 'PC2']].transform('mean')
comp['distancia'] = np.hypot(comp['PC1'] - centro['PC1'], comp['PC2'] - centro['PC2'])
print("\nVentanas mas alejadas del centro de su clase:")
print(comp.sort_values('distancia', ascending=False).head(3).round(2).to_string(index=False))

# Piezas raras: mismas caracteristicas, MISMO escalador y MISMO PCA (no se reajustan)
anom = None
if os.path.exists('datos/anomalias.csv'):
    anomalias = pd.read_csv('datos/anomalias.csv')
    anom = pca.transform(escalador.transform(anomalias[X.columns]))

pc1, pc2 = pca.explained_variance_ratio_ * 100
plt.figure(figsize=(7, 5.5))
for i, c in enumerate(sorted(y.unique())):
    m = (y == c).to_numpy()
    plt.scatter(componentes[m, 0], componentes[m, 1], label=c, color=f'C{i}', alpha=0.8)
if anom is not None:
    plt.scatter(anom[:, 0], anom[:, 1], marker='x', s=80, color='red', label='anomalia')
plt.xlabel(f'PC1 ({pc1:.1f} % de la varianza)')
plt.ylabel(f'PC2 ({pc2:.1f} % de la varianza)')
plt.title('PCA de mis caracteristicas')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
os.makedirs('figuras', exist_ok=True)
plt.savefig('figuras/pca.png', dpi=150)
print("Figura: figuras/pca.png")
