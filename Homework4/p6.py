import A
import B
import timeit
from nltk.corpus import comtrans
def p4(aligned_sents):
    for num in range(1,10):
        ibm1 = A.create_ibm1(aligned_sents, num)
        print 'num', num
        t1 = timeit.default_timer() 
        avg_aer1 = A.compute_avg_aer(aligned_sents, ibm1, 50)
        print 'ibm1: ', avg_aer1
        t2 = timeit.default_timer() 
        print 'time', t2-t1
        
        ibm2 = A.create_ibm2(aligned_sents, num)
        avg_aer2 = A.compute_avg_aer(aligned_sents, ibm2, 50)
        t3 = timeit.default_timer()
        print 'ibm2: ', avg_aer2
        print 'time:', t3 -t2
def main(aligned_sents):
    imb2 = A.create_ibm2(aligned_sents)
    ba = B.BerkeleyAligner(aligned_sents,10)
    n = len(aligned_sents)
    for i in range(n):
        my_sent = aligned_sents[i]
        imb_sent = imb2.align(my_sent)
        ba_sent = ba.align(my_sent)
        aers_imb = my_sent.alignment_error_rate(imb_sent)
        aers_ba = my_sent.alignment_error_rate(ba_sent)
        if aers_imb > aers_ba:
            print my_sent.alignment
            print my_sent.words
            print my_sent.mots
            print imb_sent.alignment
            print ba.alignment
aligned_sents = comtrans.aligned_sents()[:350]
p4(aligned_sents) 
