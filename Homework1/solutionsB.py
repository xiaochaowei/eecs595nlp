import sys
import nltk
import math
import time
from  collections import Counter

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000

# TODO: IMPLEMENT THIS FUNCTION
# Receives a list of tagged sentences and processes each sentence to generate a list of words and a list of tags.
# Each sentence is a string of space separated "WORD/TAG" tokens, with a newline character in the end.
# Remember to include start and stop symbols in yout returned lists, as defined by the constants START_SYMBOL and STOP_SYMBOL.
# brown_words (the list of words) should be a list where every element is a list of the tags of a particular sentence.
# brown_tags (the list of tags) should be a list where every element is a list of the tags of a particular sentence.
def split_wordtags(brown_train):
    brown_words = []
    brown_tags = []
    for sentence in brown_train:
        word_tags = sentence.replace('\r\n', STOP_SYMBOL+'/'+STOP_SYMBOL).split(' ')
#ADD START AND STOP
        words = []
        tags = []
        words.append(START_SYMBOL)
        words.append(START_SYMBOL)
        tags.append(START_SYMBOL)
        tags.append(START_SYMBOL)
        for wt in word_tags:
            tmp = wt.split('/')
            word = '/'.join(tmp[0:-1])
            tag = tmp[-1]
            words.append(word)
            tags.append(tag)
        brown_words.append(words)
        brown_tags.append(tags)
    return brown_words, brown_tags


# TODO: IMPLEMENT THIS FUNCTION
# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags):
    q_values = {}
    trigram_c = Counter()
    bigram_c = Counter()
    for tags in brown_tags:
        tag_tuple = tuple(tags)
        bigram_c[tag_tuple[0:2]] += 1
        for i in range(2, len(tag_tuple)):
            trigram_c[tag_tuple[i-2:i+1]] += 1
            bigram_c[tag_tuple[i-1:i+1]] += 1
#    print list(trigram_c.elements())
    print 'end'
    q_values = { item : math.log( trigram_c[item] / float(bigram_c[item[0:2]]), 2) for item in list(trigram_c) }
    print q_values[('*', '*', 'ADJ')], q_values[('ADJ','.','X')], q_values[('NOUN', 'DET', 'NOUN')]
    print "Home "
    print q_values[('CONJ','ADV','ADP')], q_values[('DET', 'NOUN', 'NUM')], q_values[('NOUN', 'PRT', 'PRON')]
    return q_values

# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values, filename):
    outfile = open(filename, "w")
    trigrams = q_values.keys()
    trigrams.sort()  
    for trigram in trigrams:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FREQ)
# brown_words is a python list where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words):
   # known_words = set([])
    known_words = []
    words_c = Counter()
    for words in brown_words:
        for word in words:
            words_c[word] += 1
    for item in list(words_c):
        if words_c[item] > RARE_WORD_MAX_FREQ:
            known_words.append(item)
    assert len(known_words) == len(set(known_words))
    known_words = set(known_words)
    return known_words

# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words, known_words):
    #brown_words_rare = []
    for idx, words in enumerate(brown_words):
        for jdx, word in enumerate(words):
            if not word in known_words:
                brown_words[idx][jdx] = '_RARE_'
    brown_words_rare = brown_words 
    return brown_words_rare

# This function takes the ouput from replace_rare and outputs it to a file
def q3_output(rare, filename):
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set
def calc_emission(brown_words_rare, brown_tags):
    e_value_c = Counter()
    tags = []
    word_num = 0
    word_c= Counter()
    tag_c = Counter()
    for idx, words in enumerate(brown_words_rare):
        for jdx, word in enumerate(words):
            e_value_c[(word, brown_tags[idx][jdx])] += 1
            tags.append(brown_tags[idx][jdx])
            word_c[word] += 1
            tag_c[brown_tags[idx][jdx]] += 1
    e_values = {}
    e_values = {item : math.log( e_value_c[item] / float(tag_c[item[1]]), 2) for item in list(e_value_c) }
    print e_values[('America', 'NOUN')]
    print e_values[('Columbia', 'NOUN')]
    print e_values[('New', 'ADJ')]
    print "** start"
    print e_values[('*', '*')]
    print e_values[('Night', 'NOUN')]
    print e_values[('Place', 'VERB')]
    print e_values[('prime', 'ADJ')]
    print e_values[('STOP', 'STOP')]
    print e_values[('_RARE_', 'VERB')]
    taglist = set(tags)
    return e_values, taglist

# This function takes the output from calc_emissions() and outputs it
def q4_output(e_values, filename):
    outfile = open(filename, "w")
    emissions = e_values.keys()
    emissions.sort()  
    for item in emissions:
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# This function takes data to tag (brown_dev_words), a set of all possible tags (taglist), a set of all known words (known_words),
# trigram probabilities (q_values) and emission probabilities (e_values) and outputs a list where every element is a tagged sentence 
# (in the WORD/TAG format, separated by spaces and with a newline in the end, just like our input tagged data)
# brown_dev_words is a python list where every element is a python list of the words of a particular sentence.
# taglist is a set of all possible tags
# known_words is a set of all known words
# q_values is from the return of calc_trigrams()
# e_values is from the return of calc_emissions()
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. Remember also that the output should not contain the "_RARE_" symbol, but rather the
# original words of the sentence!
def viterbi(brown_dev_words, taglist, known_words, q_values, e_values):
    taggeds = []
    for sentence in brown_dev_words:
        n = len(sentence)
        tagged = ['*' for i in range(n)]
        pi =[{tag:{ tag1:LOG_PROB_OF_ZERO for tag1 in taglist} for tag in taglist}  for i in range(n+1)]
        bp =[{tag:{ tag1:'*' for tag1 in taglist} for tag in taglist}  for i in range(n+1)]
        #taglist.remove('*')
        #taglist.remove('STOP')
        taglist_list = [taglist for i in range(n+2)]
        taglist_list[0] = ['*']
        taglist_list[1] = ['*']
        pi[0]['*']['*'] =0
        for k in range(1,n+1):
            orig_word = sentence[k-1]
            if not orig_word in known_words:
                word = '_RARE_'
            else:
                word = orig_word
            for v in taglist_list[k+1]:
                try:
                    e_values[(word,v)]
                except:
                    continue
                for u in taglist_list[k]:
                    max_prob = LOG_PROB_OF_ZERO * 2 
                    for w in taglist_list[k-1]:
                        try:
                            q_values[(w,u,v)]
                        except Exception as e:
                            q_values[(w,u,v)] = LOG_PROB_OF_ZERO
                            continue
                        try:
                            e_values[(word, v)]
                        except Exception as e:
                            continue 
                        prob = pi[k-1][w][u] + q_values[(w,u,v)] + e_values[(word, v)]
                        if max_prob <= prob:
                            max_prob = prob
                            pi[k][u][v] = prob
#                            tagged[k-1] = orig_word + '/' + v
                            bp[k][u][v] = w
                            #taglist_list[k+1] = [v]
#        print " ".join(tagged)
        max_prob = LOG_PROB_OF_ZERO * 2
        for v in taglist:
            for u in taglist:
                try: 
                    q_values[(u,v,'STOP')]
                except:
                    q_values[(u,v,'STOP')] = LOG_PROB_OF_ZERO
                    continue

                tmp = pi[n][u][v] + q_values[(u,v,'STOP')]
                if max_prob < tmp:
            
                    max_prob = tmp
                    tagged[n-1] = v
                    tagged[n-2] = u
        #print tagged[n-1], tagged[n-2]
        for k in range(n-2, 0,-1):
            tagged[k-1] = bp[k+2][tagged[k]][tagged[k+1]]
        tmp = ""
        for k in range(0, n):
            tagged[k] = sentence[k] + '/' + tagged[k]
        taggeds.append(" ".join(tagged) + '\r\n')
#    taggeds[-1] = taggeds[-1][:-2]
    return taggeds

# This function takes the output of viterbi() and outputs it to file
def q5_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# This function uses nltk to create the taggers described in question 6
# brown_words and brown_tags is the data to be used in training
# brown_dev_words is the data that should be tagged
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. 
def nltk_tagger(brown_words, brown_tags, brown_dev_words):
    # Hint: use the following line to format data to what NLTK expects for training
    training = [ zip(brown_words[i],brown_tags[i]) for i in xrange(len(brown_words)) ]
    default_tagger = nltk.DefaultTagger('NOUN')
    bigram_tagger = nltk.BigramTagger(training, backoff = default_tagger)
    trigram_tagger = nltk.TrigramTagger(training, backoff = bigram_tagger)
    tagged = []
    for sentence in brown_dev_words:
        tag_sentence = trigram_tagger.tag(sentence) 
    # IMPLEMENT THE REST OF THE FUNCTION HERE
        tagged.append(" ".join([ "/".join(list(item)) for item in tag_sentence]) + "\r\n")
    return tagged

# This function takes the output of nltk_tagger() and outputs it to file
def q6_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    # start timer
    time.clock()

    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    # split words and tags, and add start and stop symbols (question 1)
    brown_words, brown_tags = split_wordtags(brown_train)

    # calculate tag trigram probabilities (question 2)
    q_values = calc_trigrams(brown_tags)

    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')

    # calculate list of words with count > 5 (question 3)
    known_words = calc_known(brown_words)

    # get a version of brown_words with rare words replace with '_RARE_' (question 3)
    brown_words_rare = replace_rare(brown_words, known_words)

    # question 3 output
    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")

    # calculate emission probabilities (question 4)
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)

    # question 4 output
    q4_output(e_values, OUTPUT_PATH + "B4.txt")

    # delete unneceessary data
    del brown_train
    del brown_words_rare

    # open Brown development data (question 5)
    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    # format Brown development data here
    brown_dev_words = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])

    # do viterbi on brown_dev_words (question 5)
    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)

    # question 5 output
    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')

    # do nltk tagging here
    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words)

    # question 6 output
    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')

    # print total time to run Part B
    print "Part B time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
