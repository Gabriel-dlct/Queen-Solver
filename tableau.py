import matplotlib.pyplot as plt
import numpy as np

# matrice exemple
n = 5
mat = np.random.rand(n, n)

# positions des croix (i,j)
crosses = [(0, 1), (2, 3), (4, 4)]

plt.imshow(mat, cmap='viridis')  # couleur de fond
plt.colorbar()

# ajouter des croix
for i, j in crosses:
    plt.scatter(j, i, marker='x', color='red', s=100, linewidths=2)  # s = taille

plt.show()
