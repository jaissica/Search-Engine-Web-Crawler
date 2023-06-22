import json
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords


#Step 2: Data and query processing
ps = PorterStemmer()


stopWords = stopwords.words("english")


# Data tokenizing, lowercase and removing stopwords without stemming

def r_data_unstemmed(data_file):
    doc_id=[]
    doc_data=[]
    f = open('parsed_data.json')
    data = json.load(f)
    c = 0
    for key, value in data.items():
        sentence = sent_tokenize(value)
        final = [[token.lower() for token in sentence.split(" ")
                  if token not in stopWords] for sentence in sentence if sentence not in stopWords]
        documents = [" ".join(sentence) for sentence in final if sentence not in stopWords]
        value = ' '.join(documents)
        doc_id.append(key)
        doc_data.append(value)
        c = c + 1
        #print(c)
    f.close()
    return doc_id, doc_data




def s_data_unstemmed(key, value):
    data = dict(zip(key, value))
    with open('data_unstemmed.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)




# Data tokenizing, lowercase and removing stopwords with stemming
def r_data_stemmed(data_file):
    doc_id=[]
    doc_data=[]
    f = open('parsed_data.json')
    data = json.load(f)
    c = 0
    for key, value in data.items():
        sentence = sent_tokenize(value)
        final = [[ps.stem(token) for token in sentence.split(" ")
                  if token not in stopWords] for sentence in sentence if sentence not in stopWords]
        documents = [" ".join(sentence) for sentence in final if sentence not in stopWords]
        value = ' '.join(documents)
        doc_id.append(key)
        doc_data.append(value)
        c = c + 1
        #print(c)
    f.close()
    return doc_id, doc_data


def s_data_stemmed(doc_id, doc_data):
    data = dict(zip(doc_id, doc_data))
    #print(data)
    with open('data_stemmed.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)





#Reading queries for tokenizing, lowercase and removing stopwords without stemming
def r_queries_unstemmed(file_name):
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
            final = [[token.lower() for token in sentence.split(" ")
                      if token not in stopWords] for sentence in sentence if sentence not in stopWords]
            documents = [" ".join(sentence) for sentence in final if sentence not in stopWords]
    return documents, q_id



def s_query_unstemmed(documents, q_id):
    data = dict(zip(q_id, documents))
    with open('unstemmed_queries.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)




#Reading queries for tokenizing, lowercase and removing stopwords with stemming
def r_queries_stemmed(file_name):
    queries = []
    queries_id = []
    value = []
    with open("./" + file_name, "r") as f:
        for i in f.readlines():
            queries.append(re.findall("[A-Z|a-z].*[a-z]", i))
            queries_id.append(re.findall("^[0-9]+", i))
            sentence = [x for xs in queries for x in xs]
            q_id = [x for xs in queries_id for x in xs]
            final = [[ps.stem(token) for token in sentence.split(" ")
                      if token not in stopWords] for sentence in sentence if sentence not in stopWords]
            documents = [" ".join(sentence) for sentence in final if sentence not in stopWords]
    return documents, q_id




def s_query_stemmed(documents, q_id):
    data = dict(zip(q_id, documents))
    with open('stemmed_queries.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)



def main():
    file_name = "query_desc.51-100.short.txt"
    data_file = "parsed_data.json"
    key,value = r_data_unstemmed(data_file)
    s_data_unstemmed(key,value)
    doc_id,doc_data=r_data_stemmed(data_file)
    s_data_stemmed(doc_id, doc_data)
    documents, q_id = r_queries_unstemmed(file_name)
    s_query_unstemmed(documents, q_id)
    documents, q_id = r_queries_stemmed(file_name)
    s_query_stemmed(documents, q_id)


main()
