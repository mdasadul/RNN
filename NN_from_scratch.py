import numpy as np
import sklearn.datasets
import sklearn
import matplotlib.pyplot as plt

#Generate a dataset and ploat it
np.random.seed(0)
X,y = sklearn.datasets.make_moons(200,noise=0.20)
plt.scatter(X[:,0],X[:,1],s=40,c=y,cmap=plt.cm.Spectral)
plt.show()
#plt.scatter(X[:,0], X[:,1], s=40, c=y, cmap=plt.cm.Spectral)

