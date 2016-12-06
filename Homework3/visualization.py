from dependencyRNN import DependencyRNN
import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn import manifold

fname = 'random_init.npz'
#drnn = DependencyRNN.load(fname)
#answers = drnn.answers()
with open(fname + '.json', 'r') as fid:
    answers = json.load(fid)
#print answers
print 'load success'
ans = []
matrix = []
for i in answers:
    ans.append(i)
    matrix.append(answers[i])

m = np.asarray(matrix)
tsne = manifold.TSNE(n_components = 2, perplexity = 30.0)
x_reduced = tsne.fit_transform(m)
(nrows, ncols) = x_reduced.shape
print 'reduce success'
fig, ax = plt.subplots()
idxs = np.random.permutation(nrows)[0:50]
ax.scatter(x_reduced[:,0], x_reduced[:,1])
for i in idxs:
    ax.annotate(ans[i], (x_reduced[i,0], x_reduced[i,1]))
plt.savefig('tsne_visulization.png')
plt.show()


