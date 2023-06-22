import json
import math
from heapq import nlargest
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from nltk import PorterStemmer
from nltk.corpus import stopwords

#Step 6 Pseudo Relevance Feedback



cachedStopWords = stopwords.words("english")
ps = PorterStemmer()
#Pseudo Relevance ES


# Config Elastic Search
es = Elasticsearch([{"host": "localhost"}], timeout=1000)
indices = IndicesClient(es)


index = "ap_dataset"


f = open("./queries_pseudo.json")
queries = json.load(f)
#print(queries)


f= open("./queries_new.json")
query_number=list(json.load(f).keys())


t = open("./parsed_data.json")
parsed_data = list(json.load(t).keys())
#print(parsed_data)


g = open("./es_ind_data.json")
doc_data = json.load(g)
#print(doc_data,"\n")


t=open("./es_ind_stat.json")
index_stat=json.load(t)
#print(index_stat,"\n")




index="ap_dataset"
def query_token(data):
    body = {
        "tokenizer": "standard",
        "text": data
    }
    token = indices.analyze(index=index, body=body)
    #print("token : ",token)
    return token




def token_c(tok_list, token):
    count = 0
    for t in tok_list:
        if t == token:
            count += 1
    #print(i)
    return count



# To retrieve top scored documents.

def retriveDocs(k):
    f = open('./bm25_model_result.txt', 'r')
    docNo = []
    i = 0
    for line in f:
        # print("a" + line.split()[3].strip() + "a")
        if (i < k):
            i += 1
            docNo.append(line.split()[2])
    return docNo



#To find the relevant terms from top ranked documents.

def find_distinctive_words_in_doc(docs):
    docNo=docs

    #print("docNo : ",docNo)
    #print("parsed_data",parsed_data)
    term_rarities = {}
    new_terms = []
    # print(docs)
    # For each document, get the vector
    for doc in parsed_data:

        # for doc in tqdm(parsed_data):
        # print(doc) #doc id AP..

        tv = doc_data[doc]
        # print(tv) # full data in the index stat file
        # print(tv['term_vectors']) #has all the term vectors details

        if "text" not in tv['term_vectors']:
            continue
        for term in query_tokenized:
            #print(token) #has query term(one word)
            if term not in terms:
                tf = 0

            total_freq = index_stat["term"][token]["ttf"]
            #print("ttf: "+token+" "+str(ttf))
            doc_freq = index_stat["term"][token]["dtf"]
            # print(total_freq,doc_freq)
            # break
        rarity = doc_freq/total_freq
        if total_freq != 1:
            term_rarities[term] = rarity

        # Get the 2 rarest terms
        new_terms = nlargest(2, term_rarities, key=term_rarities.get)
    return new_terms



def es_built_in_query(query_number, new_terms_a,filename):
    for query_number in query_id:
        query=queries



def run_retrieval_models_with_relevance_feedback(query_number, query_term_list):
    original_doc_ids= retriveDocs(doc)

    new_terms_a = find_distinctive_words_in_doc(original_doc_ids)
    new_terms_a = new_terms_a + query_term_list
    es_built_in_query(query_number, new_terms_a, "./queries_new.json")




#bm25
def compute_bm(tfd, ld, avg_lg, dtf, tfq):
    k1 = 1.2
    k2 = 100
    b = 0.75
    return math.log((84678 + 0.5) / (dtf + 0.5)) * (
                (tfd + (k1 * tfd)) / (tfd + (k1 * ((1 - b) + (b * (ld / avg_lg)))))) * ((tfq + (k2 * tfq)) / (tfq + k2))


score = {"bm25": []}


for query_id, query in queries.items():
    query_tok_details = query_token(query)
    #print(query_id, ": ",query_tok_details)
    query_tokenized = [(tok['token']) for tok in query_tok_details['tokens']]
    #print(query_tokenized,"\n")
    doc_id = set()

    score_bm25_list = []

    for doc in parsed_data:

    #for doc in tqdm(parsed_data):
        #print(doc) #doc id AP..

        tv = doc_data[doc]
        #print(tv) # full data in the index stat file
        #print(tv['term_vectors']) #has all the term vectors details

        if "text" not in tv['term_vectors']:
            continue
        terms = tv['term_vectors']['text']['terms']
        #print(terms) #has doc_freq, ttf, term_freq of all the terms
        score_bm25 = 0

        #print(query_tokenized) #has list of all ther terms in query
        for token in query_tokenized:
            #print(token) #has query term(one word)
            if token not in terms:
                tf = 0
            else:
                tf = terms[token]["term_freq"]
                #print(token,terms[token]) #has the doc_freq, ttf, term_freq of a token
                #print(tf)
            #print("indexed_data ",indexed_data)
            #print("terms[token]",terms[token])
            ttf = index_stat["term"][token]["ttf"]
            #print("ttf: "+token+" "+str(ttf))
            tdf = index_stat["term"][token]["dtf"]
            #print("dtf :"+token+" "+str(tdf))

            tfq = token_c(query_tokenized, token)

            doc_id.add(doc)

            ld = index_stat["doc"][doc]
            #print("ld : ",ld,"\n")

            avg_lg = index_stat["stat"]["avg_doc_length"]
            #print("avg_ld",avg_lg,"\n")

            vocab = index_stat["stat"]["tot_num_words"]
            # print("vocab",vocab,"\n")


            score_bm25 = score_bm25 + compute_bm(tf, ld, avg_lg, tdf, tfq)


        score_bm25_list.append([score_bm25, doc, query_id])



    score_bm25_list.sort(reverse=True)
    score_bm25_list = score_bm25_list[:1000]


    score["bm25"].extend(score_bm25_list)
    # print("bm25 :",score["bm25"],"\n")



for key in score.keys():
    query_doc_es = [str(arr[2]) + " Q0 " + arr[1] + ' ' + str(i + 1) + ' ' + str(arr[0]) + ' Exp\n' for i, arr in
                    enumerate(score[key])]
    file = open(key + "_pseudo_rel_1_result.txt", "w")
    file.writelines(query_doc_es)
    file.close()



filename="./queries_new.json"
docs=retriveDocs(2)
new_terms= find_distinctive_words_in_doc(docs)
es_built_in_query(query_number,new_terms,filename)
