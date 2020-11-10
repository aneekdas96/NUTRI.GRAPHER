import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import rbf_kernel

embed = np.load("embed.npz")["store"]
print(embed)
print(embed.shape)

mins = np.min(embed,axis=0)
print(mins)

embed[:,0] += abs(mins[0])
embed[:,1] += abs(mins[1])
embed[:,2] += abs(mins[2])

print(embed)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(embed[:,0],embed[:,1],embed[:,2])
plt.show()

embed = rbf_kernel(embed)

print(embed.shape)

ax.scatter(embed[:,0],embed[:,1],embed[:,2])
plt.show()

