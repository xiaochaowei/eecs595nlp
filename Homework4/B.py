import nltk
import A
import numpy as np
from nltk.align import Alignment
from nltk.align import AlignedSent
from collections import defaultdict
import math 
class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.MIN_PROB = 1e-10
        self.t, self.q = self.train(align_sents, num_iter)
    # TODO: Computes the alignments for align_sent, using this model's parameters. Return
    #       an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, align_sent):
        l = len(align_sent.mots)
        m = len(align_sent.words)
        best_alignment = []
        for j, trg_word in enumerate(align_sent.mots):
            best_prob = self.MIN_PROB
            best_alignment_point = None
            for i, src_word in enumerate(align_sent.words):
                align_prob = self.t['f'][(src_word, trg_word)] * self.q['f'][(j+1, i+1, l,m)] + self.t['e'][(trg_word, src_word)] * self.q['e'][(i+1, j+1, m, l)]

#               align_prob = self.t['f'][(src_word, trg_word)] * self.q['f'][(j+1, i+1, l,m)]

                if align_prob > best_prob:
                    best_prob = align_prob
                    best_alignment_point = i
            if best_alignment_point != None:
                best_alignment.append((best_alignment_point, j))
        new_sent = AlignedSent(align_sent.words, align_sent.mots, Alignment(best_alignment))
#               
#        for j, trg_word in enumerate(align_sent.words):
#            best_prob = (self.t['f'][(trg_word, 'None')] * self.q['f'][(0, j+1, l, m)])
#            best_prob = max(best_prob, self.MIN_PROB)
#            best_prob = self.MIN_PROB
#            best_alignment_point = None
#            for i, src_word in enumerate(align_sent.mots):
#                align_prob = self.t['f'][(trg_word, src_word)] * self.q['f'][(i+1, j+1, l, m)] * self.t['e'][(src_word, trg_word)] * self.q['e'][(j+1, i+1, m, l)]
#                align_prob =  self.t['f'][(trg_word, src_word)] * self.q['f'][(i+1, j+1, l, m)]
#                if align_prob > best_prob:
#                    best_prob = align_prob
#                    best_alignment_point = i
#            if best_alignment_point != None:
#                best_alignment.append((j, best_alignment_point))
#        new_sent = AlignedSent(align_sent.words, align_sent.mots, Alignment(best_alignment))
#        align_sent.alignment = Alignment(best_alignment)
        return new_sent
    # TODO: Implement the EM algorithm. num_iters is the number of iterations. Returns the 
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):
        t_f = defaultdict( lambda : 0.0)
        t_e = defaultdict( lambda : 0.0)
        q_e = defaultdict( lambda : 0.0)
        q_f = defaultdict( lambda : 0.0)
        n_e = defaultdict( lambda : 0.0)
        n_f = defaultdict( lambda : 0.0)
        
        for sentence in aligned_sents:
            len_mots = len(sentence.mots)
            len_words = len(sentence.words)
            for e in set(sentence.words):
                n_e[e] += len_mots
                n_e['None'] += len_mots
            for f in set(sentence.mots):
                n_f[f] += len_words
                n_f['None'] += len_words
        # t_f = IBMModel1(aligned_sents, 10).translation_table
          
        for sentence in aligned_sents:
            for e in sentence.words:
                for f in sentence.mots:
#                    t_e[(f,e)] = 1.0 / float(n_f[f])
#                    t_f[(e,f)] = 1.0 / float(n_e[e])
#                    t_e[(f,e)] = 1.0 / float(n_e[e])
#                    t_f[(e,f)] = 1.0 / n_f[f]
                    t_e[(f,e)] = 1.0 / n_e['None']
                    t_f[(e,f)] = 1.0 / n_f['None']
                    t_e[(f, 'None')] = 1.0 / n_e['None']
                    t_f[(e, 'None')] = 1.0 / n_f['None']
            m = len(sentence.mots)
            l = len(sentence.words)
            for i in range(m+1):
                for j in range(l+1):
                    if i == 0 and j == 0:
                        continue
                    q_e[(j,i,l,m)] = 1.0 / float(l + 1)
                    q_f[(i,j,m,l)] = 1.0 / float(m + 1)
        for s in range(num_iters):
            c_f = defaultdict( lambda : 0.0)
            c_e = defaultdict( lambda : 0.0)
            total_e = defaultdict( float)
            total_f = defaultdict(float)
            for sentence in aligned_sents:
                m = len(sentence.mots)
                l = len(sentence.words)
                e = sentence.words
                f = sentence.mots
                total_e = np.zeros(m+1, dtype = np.float)
                total_f = np.zeros(l+1, dtype=  np.float)
                ws = ['None'] + e
                ms = ['None'] + f
                for i in range(1, l+1):
                    total_f[i] = 0
                    for j in range(0, m+1):
                        total_f[i] += q_f[(j, i, m, l )] * t_f[(ws[i], ms[j])]
                for j in range(1, m+1):
                    total_e[j] = 0
                    for i in range(0, l+1):
                        total_e[j] += q_e[(i, j, l, m)] * t_e[(ms[j], ws[i])]

#                for i in range( m + 1):
#                    for j in range(l + 1):
#                        if i != 0:
#                            total_e[i] += q_e[(j,i,l,m)] * t_e[(ms[i], ws[j])]
#                        if j != 0:
#                            total_f[j] += q_f[(i,j,m,l)] * t_f[(ws[j], ms[i])]
                        #total_mots[i] += q[(j,i,l,m)] * t[(f[i], e[j])]
                        #total_words[i] += q[(i,j,m,l)] * t[(e[j], f[i])]
                for i in range(m+1):
                    for j in range(l+1):
                        if i==0 and j == 0:
                            continue
#                        if i != 0:
                        if not total_e[i] == 0:
                            theta1 = q_e[(j,i,l,m)] * t_e[(ms[i],ws[j])] * 1.0 / total_e[i]
                        else:
                            theta1 = self.MIN_PROB
                        if not total_f[j] == 0:
                            theta2 = q_f[(i,j,m,l)] * t_f[(ws[j],ms[i])] * 1.0 / total_f[j]
                        else:
                            theta2 = self.MIN_PROB
                        theta = 0.5 * theta1 + 0.5 * theta2
#                        theta = math.sqrt(theta1 + theta2)
                        c_f[(ws[j], ms[i])] += theta
                        c_e[(ms[i], ws[j])] += theta
                        c_f[ms[i]] += theta
                        c_e[ws[j]] += theta
                        c_f[(i,j,m,l)] += theta
                        c_e[(j,i,l,m)] += theta
                        c_f[(j,m,l)] += theta
                        c_e[(i,l,m)] += theta
                        
            ws = []
            ms = []
            for sentence in aligned_sents:
                ws = ['None'] + sentence.words
                ms = ['None'] + sentence.mots
                l = len(sentence.words)
                m = len(sentence.mots)
            
                for i in range(m+1):
                    for j in range(l+1):
                        if i == 0 and j == 0:
                            continue
                        if c_f[(i,j,m,l)] >0 and not c_f[(j,m,l)] == 0:
                            q_f[(i,j,m,l)] = 1.0 * c_f[(i,j,m,l)] / c_f[(j,m,l)]
                        if c_e[(j,i,l,m)] > 0 and not c_e[(i,l,m)] ==0:
                            q_e[(j,i,l,m)] = 1.0 * c_e[(j,i,l,m)] / c_e[(i,l,m)]
            
#                        if c_e[(i,l,m)] == 0:
#                            q_e[(j,i,l,m)] = c_e[(j,i,l,m)] * 1.0 / c_e[(i,l,m)]
#                        if not c_f[(j,m,l)] == 0:
#                            q_f[(i,j,m,l)] = c_f[(i,j,m,l)] * 1.0 / c_f[(j,m,l)]
                        if c_e[(ms[i], ws[j])] >0 and not c_e[ws[j]] == 0:
                            t_e[(ms[i], ws[j])] = 1.0 * c_e[(ms[i], ws[j])] / c_e[ws[j]]
                        if c_f[(ws[j], ms[i])] >0 and not c_f[ms[i]] == 0:
                            t_f[(ws[j], ms[i])] = 1.0 * c_f[(ws[j], ms[i])] / c_f[ms[i]]

#                        t_e[(ms[i], ws[j])] = 1.0 * c_e[(ms[i], ws[j])] / c_e[ws[j]]
#                        t_f[(ws[j], ms[i])] = 1.0 *  c_f[(ws[j], ms[i])] / c_f[ms[i]]
        t = {}
        q = {}
        t['f'] = t_f
        q['f'] = q_f
        t['e'] = t_e
        q['e'] = q_e
#        t = t_f
#        q =  q_f                                        
        return (t,q)

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
