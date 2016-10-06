
import math
import nltk
import time
from nltk.util import ngrams 
# Constants to be used by you when you fill the functions
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000
# TODO: IMPLEMENT THIS FUNCTION
# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus):
 #   uni_tokens, bi_tokens, tr_tokens = [], [] ,[]
    unigram_tuples, bigram_tuples, trgram_tuples = [], [], []
    unigram_dir, bigram_dir, trgram_dir = {}, {}, {}
    unigram_size = 0
    for sentence in training_corpus:
        #sentence = START_SYMBOL + " " + sentence[0:-1] +  STOP_SYMBOL 
        #sentence =  
    	#token = nltk.word_tokenize(sentence)
        sentence = sentence.replace('\r\n', STOP_SYMBOL)
        #print sentence
        gram_tuples = [START_SYMBOL, START_SYMBOL]
        gram_tuples.extend(sentence.split(' '))
        gram_tuples = tuple(gram_tuples)
        unigram_size += len(gram_tuples) - 2

        for i in range(2 , len(gram_tuples)):
            if unigram_dir.has_key(gram_tuples[i:i+1]):
                unigram_dir[gram_tuples[i:i+1]] += 1
            else:
                unigram_dir[gram_tuples[i:i+1]] = 1
            if bigram_dir.has_key(gram_tuples[i-1:i+1]):
                bigram_dir[gram_tuples[i-1:i+1]] += 1
            else:
                bigram_dir[gram_tuples[i-1:i+1]] = 1
            if trgram_dir.has_key(gram_tuples[i-2:i+1]):
                trgram_dir[gram_tuples[i-2:i+1]] += 1   
            else:
                trgram_dir[gram_tuples[i-2:i+1]] = 1 
    test = math.log(float(unigram_dir[("captaincy",)])/ float(unigram_size),2)
    print test
    test = math.log(float(bigram_dir[('made', 'a')]) / unigram_dir[('made',)],2)
    print test
    test = math.log(float(trgram_dir[('and', 'not', 'come')]) / bigram_dir[('and', 'not')],2)
    print test
#    unigram_p = {item : math.log2(float(unigram_tuples.count(item))/float(unigram_size)) for item in set(unigram_tuples)}
   
    unigram_p = {item : math.log(float(unigram_dir[item])/ unigram_size ,2) for item in unigram_dir}
    unigram_dir[(START_SYMBOL,)] = unigram_size
    bigram_p = {}
    for item in bigram_dir:
        if item[0] == START_SYMBOL:
            bigram_p[item] = math.log(float(bigram_dir[item]) / len(training_corpus), 2)
        else:
            bigram_p[item] = math.log(float(bigram_dir[item]) / unigram_dir[item[0:1]], 2)
#    bigram_p = {item : math.log(float(bigram_dir[item]) / unigram_dir[item[0:1]], 2) for item in bigram_dir}
    trigram_p = {}
    for item in trgram_dir:
        if item[1] == START_SYMBOL:
            trigram_p[item] = math.log(float(trgram_dir[item]) / len(training_corpus),2)
        else:
            trigram_p[item] = math.log(float(trgram_dir[item]) / bigram_dir[item[0:2]], 2)
#    trigram_p = {item : math.log(float(trgram_dir[item]) /  bigram_dir[item[0:2]],2) for item in trgram_dir}
    ##TEST 
    print 'natural: ',  unigram_p[('natural',)]
    print 'natural that', bigram_p[('natural', 'that')]
    print 'natural that he', trigram_p[('natural','that', 'he')]    
    return unigram_p, bigram_p, trigram_p

# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys.sort()
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys.sort()
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys.sort()    
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence
# ngram_p: python dictionary of probabilities of uni-, bi- and trigrams.
# n: size of the ngram you want to use to compute probabilities
# corpus: list of sentences to score. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, corpus):
    scores = []
    print 'n: ' , n
    for sentence in corpus:
        tokens = sentence.replace('\r\n', STOP_SYMBOL).split(' ')
        for i in range(0,n-1):
           tokens.insert(0, START_SYMBOL)
        token_tuples = tuple(tokens)
        score = 0
        for i in range(n-1, len(token_tuples)):
            try:
                score += ngram_p[token_tuples[i-n +1 :i+1]]
            except Exception as e:
                score = MINUS_INFINITY_SENTENCE_LOG_PROB
                break
        scores.append(score)
    return scores

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    scores = []
    idxx = 0
    for sentence in corpus:
        #print sentence
        idxx += 1
        sentence = sentence.replace('\r\n' ,  STOP_SYMBOL)
        gram_tuples = [START_SYMBOL, START_SYMBOL]
        gram_tuples.extend(sentence.split(' '))
        gram_tuples = tuple(gram_tuples)
        score = 0
#        print "tt: ", gram_tuples[-1:]
#        print unigrams[gram_tuples[-1:]]
#        print bigrams[gram_tuples[-2:]]
#        print trigrams[gram_tuples[-3:]]
#        break
        for i in range(2, len(gram_tuples)):
            try:
                score  +=   math.log( (1/3.0 * math.pow(2, unigrams[gram_tuples[i:i+1]]) + 1/3.0 * math.pow(2, bigrams[gram_tuples[i-1:i+1]]) + 1/3.0 * math.pow(2, trigrams[gram_tuples[i-2:i+1]])),2)
            except Exception as e:
                score = MINUS_INFINITY_SENTENCE_LOG_PROB
                break
        scores.append(score)
    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

# DO NOT MODIFY THE MAIN FUNCTION
def main():
    # start timer
    time.clock()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')
    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print "Part A time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
