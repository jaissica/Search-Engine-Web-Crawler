import json
import math
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient


#Step5 Models Implementation


#Config Elastic Search
es=Elasticsearch([{"host":"localhost"}],timeout=1000)


indices = IndicesClient(es)

f = open("./queries_new.json")
queries = json.load(f)
#print(queries)



t = open("./parsed_data.json")
parsed_data = list(json.load(t).keys())
#print(parsed_data)



t = open("./es_ind_data.json")
doc_data = json.load(t)
#print(doc_data)


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



def token_count(tok_list, token):
    count = 0
    for t in tok_list:
        if t == token:
            count += 1
    #print(i)
    return count


#okapitf
def otf(tfd, ld, avg_lg):
    return tfd / (tfd + 0.5 + (1.5 * (ld/avg_lg)))



#tfidf
def tfidf(tfd, ld, avg_lg, dtf):
    return otf(tfd, ld, avg_lg) * math.log(84678 / dtf)



#bm25
def bm(tfd, ld, avg_lg, dtf, tfq):
    k1 = 1.2
    k2 = 100
    b = 0.75
    return math.log((84678 + 0.5) / (dtf + 0.5)) * (
                (tfd + (k1 * tfd)) / (tfd + (k1 * ((1 - b) + (b * (ld / avg_lg)))))) * ((tfq + (k2 * tfq)) / (tfq + k2))



#lml
def lml(tfd, ld, vocab):
    return math.log((tfd + 1) / (ld + vocab))




#lmjm
def lmjm(tfd, ld, ttf, vocab):
    l = 0.94
    return math.log((l * (tfd / ld)) + ((1 - l) * (ttf / vocab)))




score = {"okapitf": [], "tfidf": [], "bm25": [], "lml": [], "lmjm": []}



for query_id, query in queries.items():
    query_tok_details = query_token(query)
    #print(query_id, ": ",query_tok_details)
    query_tokenized = [(tok['token']) for tok in query_tok_details['tokens']]
    #print(query_tokenized,"\n")
    doc_id = set()

    score_okapitf_list = []
    score_tfidf_list = []
    score_bm25_list = []
    score_lml_list = []
    score_lmjm_list = []
    for doc in parsed_data:
        #print(doc) #doc id AP..

        tv = doc_data[doc]
        #print(tv) # full data in the index stat file
        #print(tv['term_vectors']) #has all the term vectors details

        if "text" not in tv['term_vectors']:
            continue
        terms = tv['term_vectors']['text']['terms']
        #print(terms) #has doc_freq, ttf, term_freq of all the terms
        score_okapitf = 0
        score_tfidf = 0
        score_bm25 = 0
        score_lml = 0
        score_lmjm = 0

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

            tfq = token_count(query_tokenized, token)

            doc_id.add(doc)

            ld = index_stat["doc"][doc]
            #print("ld : ",ld,"\n")

            avg_lg = index_stat["stat"]["avg_doc_length"]
            #print("avg_ld",avg_lg,"\n")

            vocab = index_stat["stat"]["tot_num_words"]
            #print("vocab",vocab,"\n")

            score_okapitf =score_okapitf + otf(tf, ld, avg_lg)
            score_tfidf = score_tfidf + tfidf(tf, ld, avg_lg, tdf)
            score_bm25 = score_bm25 + bm(tf, ld, avg_lg, tdf, tfq)
            score_lml = score_lml + lml(tf, ld, vocab)
            score_lmjm = score_lmjm + lmjm(tf, ld, ttf, vocab)

        score_okapitf_list.append([score_okapitf, doc, query_id])
        score_tfidf_list.append([score_tfidf, doc, query_id])
        score_bm25_list.append([score_bm25, doc, query_id])

        if doc in doc_id:
            score_lml_list.append([score_lml, doc, query_id])
            score_lmjm_list.append([score_lmjm, doc, query_id])


    score_okapitf_list.sort(reverse=True)
    score_okapitf_list = score_okapitf_list[:1000]

    score_tfidf_list.sort(reverse=True)
    score_tfidf_list = score_tfidf_list[:1000]

    score_bm25_list.sort(reverse=True)
    score_bm25_list = score_bm25_list[:1000]

    score_lml_list.sort(reverse=True)
    score_lml_list = score_lml_list[:1000]

    score_lmjm_list.sort(reverse=True)
    score_lmjm_list = score_lmjm_list[:1000]

    score["okapitf"].extend(score_okapitf_list)

    score["tfidf"].extend(score_tfidf_list)

    score["bm25"].extend(score_bm25_list)

    score["lml"].extend(score_lml_list)

    score["lmjm"].extend(score_lmjm_list)


for key in score.keys():
    query_doc_es = [str(arr[2]) + " Q0 " + arr[1] + ' ' + str(i + 1) + ' ' + str(arr[0]) + ' Exp\n' for i, arr in
                    enumerate(score[key])]

    file = open(key + "_model_result.txt", "w+")
    file.writelines(query_doc_es)
    file.close()

