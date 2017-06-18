# WM-Final

I used word2vec to make a name-to-nickname table.
And use this table to handle the nickname problem.

1. seg.py : segment the json file to proper format for MMR.
```
    python2 seg.py json_file > out.txt
    
    e.g. python2 seg.py NBA.json > 2017.txt
```
2. MMR_Summarizer.py : use MMR to print five important and different corpus.
```
    python2 MMR_Summarizer.py gamma corpus name.txt features....(in lower case)
    
    e.g. python2 MMR_Summarizer.py 0.8 2017.txt name.txt mvp 西河
```
