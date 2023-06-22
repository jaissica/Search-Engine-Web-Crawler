from glob import glob
import json
from tqdm import tqdm
import re

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer


#Step 4
with open("./stoplist.txt") as stop_f:
    stopwords = [word.strip() for word in stop_f]
pattern = re.compile(r'\b(' + r'|'.join(stopwords) + r')\b\s*')

porter = PorterStemmer()
def stemSentence(sentence):
    token_words=word_tokenize(sentence)
    token_words
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)

f = open("saved_data.json", "r")
parsed_json = json.load(f)


doc_token_json = {}
for link, doc_text in tqdm(parsed_json.items()):

    doc_text = doc_text.replace('\n', " ")
    doc_text = pattern.sub('',doc_text)
    doc_text = stemSentence(doc_text)
    doc_token_json[link] = doc_text
    # break


save_file = open("preprocess_data.json", "w")
json.dump(doc_token_json, save_file, indent = 6)
save_file.close()