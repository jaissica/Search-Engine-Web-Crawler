import json
import time
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from elasticsearch import Elasticsearch


#step 2 stemming and removing stop words and parsing data to elasticsearch

ps = PorterStemmer()



# Config Elastic Search
es = Elasticsearch([{"host": "localhost"}], timeout=1000)

# reponse=es.indices.create(index='ap_dataset',body=request_body)

cachedStopWords = stopwords.words("english")

# Data Stemming and removing stopwords
f = open('parsed_data.json')
data = json.load(f)
c = 0
for key, value in data.items():
    sentence = sent_tokenize(value)
    final = [[ps.stem(token) for token in sentence.split(" ")
              if token not in cachedStopWords] for sentence in sentence if sentence not in cachedStopWords]
    documents = [" ".join(sentence) for sentence in final if sentence not in cachedStopWords]
    value = ' '.join(documents)
    doc_id = key
    text = value
    # print(text)
    es_data = {
        "text": text
    }
    es.index(index='ap_dataset', id=doc_id, body=es_data)
    print(key," : ",value)
    c = c + 1
    print(c)
f.close()


def clean_queries(file_name):
    queries = []
    queries_id = []
    value = []
    with open("./" + file_name, "r") as f:
        for i in f.readlines():
            queries.append(re.findall("[A-Z|a-z].*[a-z]", i))
            queries_id.append(re.findall("^[0-9]+", i))
            sentence = [x for xs in queries for x in xs]
            q_id = [x for xs in queries_id for x in xs]
            # print(q_id)
            final = [[ps.stem(token) for token in sentence.split(" ")
                      if token not in cachedStopWords] for sentence in sentence if sentence not in cachedStopWords]
            documents = [" ".join(sentence) for sentence in final if sentence not in cachedStopWords]
    return documents, q_id



def new_query_to_file(documents, q_id):
    data = dict(zip(q_id, documents))
    print(data)
    with open('queries_new.json', 'a') as outfile:
        json.dump(data, outfile, indent=2)



def main():
    file_name = "query_desc.51-100.short.txt"
    documents, q_id = clean_queries(file_name)
    new_query_to_file(documents, q_id)


main()
