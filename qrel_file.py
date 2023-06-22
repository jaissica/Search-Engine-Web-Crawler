import pandas as pd
import os

i=1
path='./data'
print(os.listdir(path))
for filename in os.listdir(path):
    df = pd.read_json (path+'/'+filename)
    df.to_csv ('qrel'+str(i)+'.txt',sep=' ', index = False)
    i=i+1

filenames = ['qrel1.txt', 'qrel2.txt', 'qrel3.txt']
with open('./qrel_raw.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)