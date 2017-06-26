#-*-coding:utf-8 -*-
from __future__ import division
import os
import math
import sys
from collections import defaultdict
import operator
from pytrends.request import TrendReq
import glob
import pandas
import time
import datetime
from dateutil import parser

# Method to compute every word's TF.IDF value in a given cluster
def TF_IDF(wF, dF):
    retval = defaultdict(float)
    for k, val in wF.iteritems():
        retval[k] = val * (1 / len(dF[k]))
    # Method variables
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
    return word

def doc_sim(query, tF, dF, dlen):
    s = 0.0
    global d_query
    for w in query:
        tmp = (tF[w] / (math.log(len(dF[w])+1))) / dlen
        if w in d_query:
            tmp *= 0
        s += tmp
    return s

def sim(query, tF, dF, dlen, doc):
    s = 0.0
    for w in query:
        try:
            s += (tF[w] / (math.log(len(dF[w])+1))) / dlen
        except:
            print w
            sys.exit()
    global avg, t_factor
    
    return s * (t_factor[doc] / avg + 1)

# Method to get the single Best matching sentence
def getBest(tF, query, dF, dlen):
    # variables to help keep track of the best file
    best_sent = None
    prev = float("-inf")
        
    # loop through all sentences
    for key, val  in tF.iteritems():
        #print val
        similarity = sim(query, val, dF, dlen[key], key)

        # take note of the best matching sentence
        if similarity > prev:
            best_sent = key
            prev = similarity
                    
    # select the chosen best matching sentence from original data
    global score_list
    score_list[best_sent] = prev
    return best_sent

# Method to find n sentences with the best MR values
def makeSummary(gamma, tF, query, best_doc, dF, doc_len, n):
    # local variables
    selected_doc = [best_doc]
    
    global score_list
    for i in range(n):
        best_line = None
        prev = float("-inf")
            
        # go through all sentences
        g2 = gamma - i* 0.025
        #g2 = gamma
        for key, val in tF.iteritems():
                    
            # get the marginal relevance of a query
            if key in selected_doc :
                continue
            curr = MR(g2, val, query, dF, doc_len[key], selected_doc, tF, key)
                    
            # set this sentence as the next best sentence if its' marginal releveance is better than the
            # current best
            if curr > prev:
                prev = curr
                best_line = key
                    
        # update our selected sentences and summary            
        selected_doc += [best_line]
        score_list[best_line] = prev
            
    return selected_doc
    
# Method to compute the MR value for a given sentence
def MR(gamma, tF, query , dF, doc_len, selected_doc, a_tF, doc):
    

    left_of_minus = gamma * sim(query, tF, dF, doc_len, doc)
    
    right_values = [float("-inf")]
        
    for d in selected_doc:
        q = []
        for key, val in a_tF[d].iteritems():
            q.append(key)
        right_values.append( (1.0 - gamma) * doc_sim(q, tF, dF, doc_len))
            
    right_of_minus = max(right_values)
        
    return left_of_minus - right_of_minus

# Method to make a summary.

#summary_length = int(sys.argv[2])
#cluster_path = sys.argv[3]

# open all files in the user specified directory
google_username = "iboom579"
google_password = "iboom579gmail"
pytrends = TrendReq(google_username, google_password, custom_useragent='My Pytrends Script')
#trend_payload = {'q': u'王柏融','date':'now 3-y', 'geo': 'TW','tz': 'Etc/GMT+8'}
pytrends.build_payload(kw_list=[u'陽岱鋼'], geo='TW', timeframe='today 5-y')
#pytrends.build_payload(kw_list=[u'王柏融'], geo='TW', timeframe='today 5-y')
#pytrends.build_payload(kw_list=[u'陽岱鋼'], timeframe='today 5-y')

try:
    #tmp = pytrends.interest_over_time()[u'王柏融'].to_dict()
    tmp = pytrends.interest_over_time()[u'陽岱鋼'].to_dict()
except:
    print pytrends
    sys.exit()

trend = defaultdict(float)

for key, val in tmp.iteritems():
    trend[key.to_pydatetime().date()] = val

start = datetime.datetime(2017,6,4)
_sum = 0
_l = []
for i in range(70):
    _sum += trend[(start-datetime.timedelta(7*i)).date()]
    _l.append(trend[(start-datetime.timedelta(7*i)).date()])
avg = _sum / 70.0
avg = max(_l)
print 'avg : ', avg
print 'max : ', max(_l)
print 'min : ', min(_l)

tF = defaultdict(lambda: defaultdict(float))
dF = defaultdict(set)
wF = defaultdict(float)
doc_len = defaultdict(float)
detail = dict()

t_factor = defaultdict(float)
cur = 0

name_list = dict()
with open(sys.argv[3]) as n:
    l = n.readlines()
    for li in l:
        li = li.split()
        name_list[li[1]] = li[0]


with open(sys.argv[2]) as f:
    l = f.readlines()
    for line in l:
        line = line.split('//*//')
        if line[0] == ' ':
            continue
        other = []
        other.append(line[0])
        other.append(line[1])
        other.append(line[2])
        other.append(line[3])
        detail[cur] = other
        content = line[1].split()
        try:
            t = parser.parse(line[2])
        except:
            print t
        t += datetime.timedelta(days=(6 - t.weekday()))
        t_factor[cur] = trend[t.date()]
        #t_factor[cur] = 10

        for word in content:
            if word in name_list:
                word = name_list[word]
            w = word.lower()
            doc_len[cur] += 1
            dF[w].add(cur)
            tF[cur][w] += 1
            wF[w] += 1
        cur += 1


#query = makeQuery(n, wF, dF)
#query = [u'Westbrook', '衛斯布魯克', '西河', '大三元', u'50', '連續', '歷史',  u'42']
#d_query = ['王柏融', '柏融', '王柏', '大王']
d_query = ['陽岱鋼', '陽岱', '鋼', 'yoh']
#d_query = ['westbrook']
for i in range(100):
    try:
        d_query.append(sys.argv[4+i])
    except:
        break

# pick a sentence that best matches our query
score_list = {}
best_doc = getBest(tF, d_query, dF, doc_len)
'''
print best_doc, detail[best_doc][0]
print detail[best_doc][1]
print detail[best_doc][3]
'''
# build a summary by adding more relevant sentences

gamma = float(sys.argv[1])
#gamma = 1.0
summary = makeSummary(gamma, tF, d_query, best_doc, dF, doc_len, 7)

for d in summary:
    print d, detail[d][0]
    print detail[d][1]
    print detail[d][2]
    print detail[d][3]
    print score_list[d]
    print t_factor[d]
    print


