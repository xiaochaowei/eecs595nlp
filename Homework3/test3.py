#chaowei xiao
from theano import pp
from theano import function
import theano 
import theano.tensor as T
import numpy as np 
def norm():
    x, t = theano.tensor.fvector('x'), theano.tensor.fvector('t')
    w1 = theano.shared(np.random.randn(3,4))
    w2 = theano.shared(np.random.randn(4,2))
    a1 = theano.tensor.tanh(theano.tensor.dot(x,w1))
    a2 = theano.tensor.tanh(theano.tensor.dot(a1,w2))
    cost2 = theano.tensor.sqr(a2 - t).sum()
    cost2 += theano.tensor.sqr(w2.sum())
    cost1 = theano.tensor.sqr(w1.sum())

    params = [[w2],[w1]]
    costs = [cost2,cost1]
    grad_ends = [[a1], [x]]

    next_grad = None
    param_grads = []
    for i in xrange(2):
        param_grad, next_grad = theano.subgraph_grad(
            wrt=params[i], end=grad_ends[i],
            start=next_grad, cost=costs[i]
        )
        next_grad = dict(zip(grad_ends[i], next_grad))
        param_grads.extend(param_grad)
    print dir(param_grads)

def norm2():
    
   # w = theano.shared(np.zeros(10))
#    print w
    w = T.dscalar()
    sigmoid = 1 / (1 + T.exp(w))
    gy = T.grad(sigmoid, w)
    print pp(gy)
#    f =  theano.function([w], sigmoid)
#    print f(np.zeros(10))
#    print dir(sigmoid)
#    print sigmoid.get_value()

norm2()
