import gensim
from gensim.models import Word2Vec
import json

import numpy as np
#parse json
fname = 'hist_split.json'

with open(fname, 'r') as fid:
    data = fid.read()
data_j = json.loads(data)
train_data = data_j['train']
sentences = []
#    print train_data[0]
for i in train_data:
    dep_sents = i[0]
    tmp = []
    for words in dep_sents:
        if words[0] == None:
            continue
        tmp.append(words[0])
    sentences.append(tmp)
model = gensim.models.Word2Vec(size=100, window=5, min_count=1)
model.build_vocab(sentences)
alpha, min_alpha, passes = (0.025, 0.001, 20)
alpha_delta = (alpha - min_alpha) / passes
for epoch in range(passes):
    model.alpha, model.min_alpha = alpha, alpha
    model.train(sentences)
    print('completed pass %i at alpha %f' % (epoch + 1, alpha))
    alpha -= alpha_delta
    np.random.shuffle(sentences)
fname = 'gensim_model1'
model.save(fname)
