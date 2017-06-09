#-*-coding:utf-8 -*-
import os
import math
import sys
from collections import defaultdict
import operator

# Method to compute every word's TF.IDF value in a given cluster
def TF_IDF(wF, dF):
    retval = defaultdict(float)
    for k, val in wF.iteritems():
        retval[k] = val * (1 / len(dF[k]))
    # Method variables
    '''
    tfs = self.sim.TFs(sentences)
        
    retval = {}

    # for every word
    for word in tfs:
        #calculate every word's tf-idf score
        tf_idfs=  tfs[word] * idfs[word]
        
        # add word and its tf-idf score to dictionary
        if retval.get(tf_idfs, None) == None:
            retval[tf_idfs] = [word]
        else:
            retval[tf_idfs].append(word)
    '''
    return retval


# Method to build a query by selecting n words with the highest TF.IDF values
def makeQuery(n, wF, dF):
    scored_words = TF_IDF(wF, dF)
    best_words = getBestWords(n, scored_words)
    return best_words

# Method to build a list of the n best words in a cluster
def getBestWords(n, score):
    s = sorted(score.items(), key=operator.itemgetter(1), reverse = True)
    word = []
    count = 0
    for w in s:
        word.append(w[0])
        count += 1
        if count >= n:
            break
    '''
    best_scores  = scored_words.keys()
    best_scores.sort()
    best_words = []

    # loop through the list in reverse order
    for i in range(-1, -n, -1):
            
        words = scored_words[best_scores[i]] #returns a list of words
        for word in words:
            if i >-n:
                best_words.append(word)
                i = i-1
    '''
    return word

def doc_sim(query, tF, dF, dlen):
    s = 0
    global d_query
    for w in query:
        if w in d_query:
            continue
        try:
            s += (tF[w] / len(dF[w])) / dlen
        except:
            print tF[w], dlen, len(dF[w]), w
            sys.exit()
    return s

def sim(query, tF, dF, dlen):
    s = 0
    for w in query:
        try:
            s += (tF[w] / len(dF[w])) / dlen
        except:
            print tF[w], dlen, len(dF[w]), w
            sys.exit()
    return s

# Method to get the single Best matching sentence
def getBest(tF, query, dF, dlen):
    # variables to help keep track of the best file
    best_sent = None
    prev = float("-inf")
        
    # loop through all sentences
    for key, val  in tF.iteritems():
        #print val
        similarity = sim(query, val, dF, dlen[key])

        # take note of the best matching sentence
        if similarity > prev:
            best_sent = key
            prev = similarity
                    
    # select the chosen best matching sentence from original data
    return best_sent


# Method to find n sentences with the best MR values
def makeSummary(gamma, tF, query, best_doc, dF, doc_len, n):
    # local variables
    selected_doc = [best_doc]
        
    for i in range(n):
        best_line = None
        prev = float("-inf")
            
        # go through all sentences
        for key, val in tF.iteritems():
                    
            # get the marginal relevance of a query
            if key in selected_doc :
                continue
            curr = MR(gamma, val, query, dF, doc_len[key], selected_doc, tF)
                    
            # set this sentence as the next best sentence if its' marginal releveance is better than the
            # current best
            if curr > prev:
                prev = curr
                best_line = key
                    
        # update our selected sentences and summary            
        selected_doc += [best_line]
            
    return selected_doc
    
# Method to compute the MR value for a given sentence
def MR(gamma, tF, query , dF, doc_len, selected_doc, a_tF):
    

    left_of_minus = gamma * sim(query, tF, dF, doc_len)
    
    right_values = [float("-inf")]
        
    for d in selected_doc:
        q = []
        for key, val in a_tF[d].iteritems():
            q.append(key)
        right_values.append( (1 - gamma) * doc_sim(q, tF, dF, doc_len))
            
    right_of_minus = max(right_values)
        
    return left_of_minus - right_of_minus

# Method to make a summary.

#summary_length = int(sys.argv[2])
#cluster_path = sys.argv[3]

# open all files in the user specified directory

tF = defaultdict(lambda: defaultdict(float))
dF = defaultdict(set)
wF = defaultdict(float)
doc_len = defaultdict(float)
detail = dict()

cur = 0
with open(sys.argv[2]) as f:
    l = f.readlines()
    for line in l:
        line = line.split('//*//')
        other = []
        other.append(line[0])
        other.append(line[1])
        other.append(line[2])
        other.append(line[3])
        detail[cur] = other
        content = line[1].split()
        for word in content:
            w = word.lower()
            doc_len[cur] += 1
            dF[w].add(cur)
            tF[cur][w] += 1
            wF[w] += 1
        cur += 1

'''
for root, dirs, files in os.walk(cluster_path):
    for name in files:
        with open(os.path.join(root, name)) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for word in content:
            word = word.split()
            for w in word:
                dF[w].add(name)
                tF[name][w] += 1
                wF[w] += 1
'''
# build a query

#query = makeQuery(n, wF, dF)
#query = [u'Westbrook', '衛斯布魯克', '西河', '大三元', u'50', '連續', '歷史',  u'42']
d_query = ['西河']
for i in range(100):
    try:
        d_query.append(sys.argv[3+i])
    except:
        break

# pick a sentence that best matches our query
best_doc = getBest(tF, d_query, dF, doc_len)
'''
print best_doc, detail[best_doc][0]
print detail[best_doc][1]
print detail[best_doc][3]
'''
# build a summary by adding more relevant sentences
gamma = float(sys.argv[1])
summary = makeSummary(gamma, tF, d_query, best_doc, dF, doc_len, 4)

for d in summary:
    print d, detail[d][0]
    print detail[d][1]
    print detail[d][2]
    print detail[d][3]


