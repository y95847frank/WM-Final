# -*- coding: utf-8 -*-
import json
import jieba
import sys
import os
from pprint import pprint
import codecs

#with codecs.open(sys.argv[1], 'r', encoding='utf-8') as f:
with open(sys.argv[1], 'r') as f:
    #data = json.load(f.decode('utf-8'))
    data = json.load(f)
for k, v in data.iteritems():
    #print k
    for i in v:
        try:
            title = i[u'article_title'][1:3]

            #if title == u'\u516c\u544a' or title == u'\u5916\u96fb' or title == u'\u5916\u7d6e':
            #    continue
            #if title != u'\u65b0\u805e':
            #    continue
            if title != u'新聞' and title != u'情報' and title != u'討論' and title != u'專欄':
                continue
            #print "{'title' : ",
            print i['article_title'].encode('utf-8'),
            c =  i[u'content']
            seg_list = jieba.cut(c)
            line = (" ".join(seg_list))
            line = line.replace('  ', ' ')
            line = line.replace('  ', ' ')
            line = line.replace('  ', ' ')
            #print " , 'content' : ",
            print '//*//',
            print line.encode('utf-8'),
            #print " , 'date' : ",
            print '//*//',
            print i['date'].encode('utf-8'),
            #print " , 'message' : ",
            print '//*//',
            print i['message_conut']
            #print ' }'
        except:
            continue
