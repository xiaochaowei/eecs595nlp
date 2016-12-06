import nltk
from nltk.align import IBMModel1, IBMModel2
# TODO: Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):
    ibm = IBMModel1(aligned_sents,10)
    return ibm

# TODO: Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
    ibm = IBMModel2(aligned_sents,10)
#    ibm = IBMModel2(aligned_sents,num)
    return ibm
# TODO: Compute the average AER for the first n sentences
#       in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):
    aers = 0.0
    for i in range(n):
        my_aligned = aligned_sents[i]     
#        print my_aligned.alignment
#        print model.align(my_aligned).alignment
        aers += my_aligned.alignment_error_rate(model.align(my_aligned))
#        print aers
#        return aers
    aers = aers /  float(n)
    return aers
# TODO: Computes the alignments for the first 20 sentences in
#       aligned_sents and saves the sentences and their alignments
#       to file_name. Use the format specified in the assignment.
def save_model_output(aligned_sents, model, file_name):
    out_str = ""
    for i in range(20):
        sent = aligned_sents[i]
        my_aligned = model.align(sent)
        out_str += str(my_aligned.words) + '\n'
        out_str += str(my_aligned.mots) +  '\n'
        out_str += str(my_aligned.alignment) + '\n'
        out_str += '\n'
    with open(file_name, 'w') as fid:
        fid.write(out_str)


def main(aligned_sents):
    ibm1 = create_ibm1(aligned_sents)
    save_model_output(aligned_sents, ibm1, "ibm1.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)

    print ('IBM Model 1')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)
    
    print ('IBM Model 2')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
