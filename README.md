# WM-Final
1. seg.py : segment the json file to proper format for MMR.
```
    python2 seg.py json_file > out.txt
    
    e.g. python2 seg.py NBA.json > 2017.txt
```
2. MMR_Summarizer.py : use MMR to print five important and different corpus.
```
    python2 MMR_Summarizer.py gamma corpus features....(in lower case)
    
    e.g. python2 MMR_Summarizer.py 0.8 2017.txt mvp 西河
```
