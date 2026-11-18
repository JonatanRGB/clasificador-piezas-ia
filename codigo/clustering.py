"""
Semana 11: agrupamiento sin etiquetas (K-Means y DBSCAN) y comparacion con mis clases.
Uso (desde la raiz del repo):  python codigo/clustering.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score

features = pd.read_csv('datos/features.csv')
X = features.drop(columns=['ventana', 'etiqueta'])
y = features['etiqueta']            # solo para comparar al final

escalador = StandardScaler().fit(X)
X_esc = escalador.transform(X)
pca = PCA(n_components=3).fit(X_esc)  # 3 componentes para ver los grupos en 3D (solo para graficar)
plano = pca.transform(X_esc)
varianza = pca.explained_variance_ratio_ * 100
print("Varianza de PC1, PC2 y PC3 (%):", np.round(varianza, 1), "| acumulada:", round(varianza.sum(), 1))

# ---------------- Bloque 1: K-Means ----------------
kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
grupos = kmeans.fit_predict(X_esc)
print("Tabla cruzada K-Means (filas = mi etiqueta, columnas = grupo):")
print(pd.crosstab(y, grupos))

# ---------------- Bloque 2: DBSCAN ----------------
print("\nDBSCAN con distintos eps (min_samples=5):")
print(f"{'eps':>5}{'grupos':>8}{'ruido':>7}")
for eps in [0.5, 0.8, 1.0, 1.2, 1.5]:
    g = DBSCAN(eps=eps, min_samples=5).fit_predict(X_esc)
    n_grupos = len(set(g)) - (1 if -1 in g else 0)
    print(f"{eps:>5}{n_grupos:>8}{list(g).count(-1):>7}")

EPS = 1.0   # el menor eps que encuentra mis 3 grupos dejando poco ruido
dbscan = DBSCAN(eps=EPS, min_samples=5)
grupos_db = dbscan.fit_predict(X_esc)
n_grupos = len(set(grupos_db)) - (1 if -1 in grupos_db else 0)
n_ruido = list(grupos_db).count(-1)
print(f"\nElegido eps={EPS}: {n_grupos} grupos, {n_ruido} puntos de ruido")
print(pd.crosstab(y, grupos_db))

# Piezas raras: mismas caracteristicas y mismo escalador, DBSCAN sobre todo junto
anomalias = pd.read_csv('datos/anomalias.csv')
X_todo = np.vstack([X_esc, escalador.transform(anomalias[X.columns])])
g_todo = DBSCAN(eps=EPS, min_samples=5).fit_predict(X_todo)
g_anom = g_todo[len(X_esc):]
g_norm = g_todo[:len(X_esc)]
detectadas = int(np.sum(g_anom == -1))
print(f"\nPiezas raras marcadas como ruido: {detectadas} de {len(anomalias)}")
print(f"Piezas normales marcadas como ruido: {int(np.sum(g_norm == -1))} de {len(X_esc)}")
tipos = pd.read_csv('datos/anomalias_tipos.csv').merge(anomalias[['ventana']], on='ventana')
tipos['es_ruido'] = g_anom == -1
print(tipos.groupby('tipo', sort=False)['es_ruido'].agg(['sum', 'count']).rename(
    columns={'sum': 'como_ruido', 'count': 'total'}))

# ---------------- Extra: numero natural de grupos ----------------
print("\nk   inercia   silueta")
inercias = []
for k in range(1, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_esc)
    inercias.append(km.inertia_)
    sil = silhouette_score(X_esc, km.labels_) if k > 1 else float('nan')
    print(f"{k}  {km.inertia_:8.1f}   {sil:.3f}")

# ---------------- Figura: el mismo espacio de PCA en 3D, tres veces ----------------
os.makedirs('figuras', exist_ok=True)
plano_anom = pca.transform(escalador.transform(anomalias[X.columns]))
fig = plt.figure(figsize=(18, 6))
ejes = [fig.add_subplot(1, 3, i, projection='3d') for i in (1, 2, 3)]


def puntos(ax, P, **kw):
    ax.scatter(P[:, 0], P[:, 1], P[:, 2], **kw)


for i, c in enumerate(sorted(y.unique())):
    m = (y == c).to_numpy()
    puntos(ejes[0], plano[m], color=f'C{i}', label=c, alpha=0.8)
ejes[0].set_title('Etiqueta real')
for g in sorted(set(grupos)):
    puntos(ejes[1], plano[grupos == g], color=f'C{g + 3}', label=f'grupo {g}', alpha=0.8)
ejes[1].set_title('K-Means (k=3)')
for g in sorted(set(g_norm)):
    m = g_norm == g
    if g == -1:
        puntos(ejes[2], plano[m], color='k', marker='^', label='ruido (normal)')
    else:
        puntos(ejes[2], plano[m], color=f'C{g + 6}', label=f'grupo {g}', alpha=0.8)
ruido = g_anom == -1
if ruido.any():
    puntos(ejes[2], plano_anom[ruido], color='red', marker='x', s=80, label='anomalia detectada')
if (~ruido).any():
    puntos(ejes[2], plano_anom[~ruido], color='red', marker='o', facecolors='none', s=80,
           label='anomalia NO detectada')
ejes[2].set_title(f'DBSCAN (eps={EPS}) con piezas raras')
for ax in ejes:
    ax.set_xlabel(f'PC1 ({varianza[0]:.1f} %)')
    ax.set_ylabel(f'PC2 ({varianza[1]:.1f} %)')
    ax.set_zlabel(f'PC3 ({varianza[2]:.1f} %)')
    ax.view_init(elev=20, azim=-60)
    ax.legend(fontsize=8, loc='upper left')
fig.suptitle(f'Espacio de PCA en 3D: {varianza.sum():.1f} % de la varianza total', fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig('figuras/clustering.png', dpi=150)

fig, a = plt.subplots(figsize=(6, 4))
a.plot(range(1, 9), inercias, 'o-')
a.set_xlabel('k')
a.set_ylabel('inercia')
a.set_title('Metodo del codo')
a.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('figuras/codo.png', dpi=150)
print("Figuras: figuras/clustering.png y figuras/codo.png")
