import json
import math
import re


#Step8(Stemmed)
def tokenize_query(query):
    body = {
        "tokenizer": "standard",
        "text": query
    }

    tokenized = re.findall(pattern=r"\w+(?:\.?\w)*", string=query)

    return tokenized


def count_token(tok_list, token):
    i = 0
    for t in tok_list:
        if t == token:
            i += 1
    return i


f = open("./stemmed_index_stat.json")
index_stat = json.load(f)


def okapiTF(tfd, ld, avg_lg):
    return tfd / (tfd + 0.5 + (1.5 * (ld / avg_lg)))


def tfidf(tfd, ld, avg_lg, dtf):
    return okapiTF(tfd, ld, avg_lg) * math.log(84678 / dtf)


def bm25(tfd, ld, avg_lg, dtf, tfq):
    k1 = 1.2
    k2 = 100
    b = 0.75
    return math.log((84678 + 0.5) / (dtf + 0.5)) * (
                (tfd + (k1 * tfd)) / (tfd + (k1 * ((1 - b) + (b * (ld / avg_lg)))))) * ((tfq + (k2 * tfq)) / (tfq + k2))


def lml_smoothing(tfd, ld, vocab):
    return math.log((tfd + 1) / (ld + vocab))


def lmjm(tfd, ld, ttf, vocab):
    l = 0.94
    return math.log((l * (tfd / ld)) + ((1 - l) * (ttf / vocab)))


f = open("./stemmed_queries.json")
query_details = json.load(f)

f = open("./inverted_index_stemmed.json", "r")
inverted_index = json.load(f)

docs = index_stat["doc"].keys()

score = {"okapitf": [], "tfidf": [], "bm25": [], "lml": [], "lmjm": []}
for qid, query in query_details.items():
    query_tokenized = tokenize_query(query)
    # query_tokenized = [(tok['token']) for tok in query_tok_details['tokens']]

    score_okapitf_list = {}
    score_tfidf_list = {}
    score_bm25_list = {}
    score_lml_list = {}
    score_lmjm_list = {}
    doc_has_query_term = {}

    doc_to_search = doc_has_query_term.keys()
    for token_in_query in query_tokenized:
        for doc_in_tok in inverted_index[token_in_query].keys():
            doc_has_query_term[doc_in_tok] = len(inverted_index[token_in_query].keys())
            score_okapitf_list[doc_in_tok] = 0
            score_tfidf_list[doc_in_tok] = 0
            score_bm25_list[doc_in_tok] = 0
            score_lml_list[doc_in_tok] = 0
            score_lmjm_list[doc_in_tok] = 0


    for doc in doc_to_search:

        for token in query_tokenized:
            if token not in inverted_index:
                tf = 0
            elif doc not in inverted_index[token]:
                tf = 0
            else:
                tf = len(inverted_index[token][doc])

            ttf = index_stat["term"][token]["ttf"]
            tdf = index_stat["term"][token]["dtf"]

            tfq = count_token(query_tokenized, token)


            ld = index_stat['doc'][doc]
            avg_lg = index_stat['stat']['avg_doc_length']
            vocab = index_stat['stat']['tot_num_words']

            score_okapitf_list[doc] += okapiTF(tf, ld, avg_lg)
            score_tfidf_list[doc] += tfidf(tf, ld, avg_lg, tdf)
            score_bm25_list[doc] += bm25(tf, ld, avg_lg, tdf, tfq)
            score_lml_list[doc] += lml_smoothing(tf, ld, vocab)
            score_lmjm_list[doc] += lmjm(tf, ld, ttf, vocab)




    score_okapitf_l = []
    score_tfidf_l = []
    score_bm25_l = []
    score_lml_l = []
    score_lmjm_l = []

    for doc in doc_to_search:
        score_okapitf_l.append([score_okapitf_list[doc],doc,qid])
        score_tfidf_l.append([score_tfidf_list[doc],doc,qid])
        score_bm25_l.append([score_bm25_list[doc],doc,qid])
        score_lml_l.append([score_lml_list[doc],doc,qid])
        score_lmjm_l.append([score_lmjm_list[doc],doc,qid])

    score_okapitf_l.sort(reverse=True)
    score_okapitf_l = score_okapitf_l[:1000]

    score_tfidf_l.sort(reverse=True)
    score_tfidf_l = score_tfidf_l[:1000]

    score_bm25_l.sort(reverse=True)
    score_bm25_l = score_bm25_l[:1000]

    score_lml_l.sort(reverse=True)
    score_lml_l = score_lml_l[:1000]

    score_lmjm_l.sort(reverse=True)
    score_lmjm_l = score_lmjm_l[:1000]

    score["okapitf"].extend(score_okapitf_l)
    score["tfidf"].extend(score_tfidf_l)
    score["bm25"].extend(score_bm25_l)
    score["lml"].extend(score_lml_l)
    score["lmjm"].extend(score_lmjm_l)


for key in score.keys():
    query_doc_es = [str(arr[2]) + " Q0 " + arr[1] + ' ' + str(i + 1) + ' ' + str(arr[0]) + ' Exp\n' for i, arr in
                    enumerate(score[key])]

    file = open("Results/"+ key + "_stemmed_uncomp_res.txt", "w+")
    file.writelines(query_doc_es)
    file.close()
