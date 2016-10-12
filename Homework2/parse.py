import sys
import random
from providedcode import dataset
from providedcode.transitionparser import TransitionParser
from providedcode.evaluate import DependencyEvaluator
from featureextractor import FeatureExtractor
from providedcode.dependencygraph import DependencyGraph
from transition import Transition
if __name__ == '__main__':
    sents = []
    model_name = sys.argv[1]
    tp = TransitionParser.load(model_name)
    for line in  sys.stdin:
        # sents.append(line)
        sentence = DependencyGraph.from_sentence(line)
        sents.append(sentence)
    parsed = tp.parse(sents)
    for p in parsed:
        print p.to_conll(10).encode('utf-8')
        	        	    
