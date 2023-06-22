import json
import math
import re


#Step9(Stemmed)
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



def bm25(tfd, ld, avg_lg, dtf, tfq):
    k1 = 1.2
    k2 = 100
    b = 0.75
    return math.log((84678 + 0.5) / (dtf + 0.5)) * (
                (tfd + (k1 * tfd)) / (tfd + (k1 * ((1 - b) + (b * (ld / avg_lg)))))) * ((tfq + (k2 * tfq)) / (tfq + k2))

def get_min_span(index, query, doc ):
    query = set(query)
    term_not_present_c = 0
    indices = []
    for token in query:
        if token in index:
            if doc in index[token]:
                indices.append(index[token][doc])
            else:
                term_not_present_c = 0

    indices_ind = [0 for i in indices]
    span = [i[0] for i in indices]
    # print(span)

    min_span = max(span) - min(span)

    while True:
        min_ind = span.index(min(span))
        if len(indices[min_ind])-1 == indices_ind[min_ind]:
            return min_span/len(indices)
        else:
            indices_ind[min_ind] += 1
            new_ind = indices_ind[min_ind]
            span[min_ind] = indices[min_ind][new_ind]
            min_span = min(min_span, max(span) - min(span))

def proximity_score(index, query, score):
    for doc in score.keys():
        min_span = get_min_span(index, query, doc)
        score[doc] += math.log(0.01 + math.exp(-min_span))

    return score



f = open("./stemmed_queries.json")
query_details = json.load(f)

f = open("./inverted_index_stemmed.json", "r")
inverted_index = json.load(f)

docs = index_stat["doc"].keys()

score = {"okapitf": [], "tfidf": [], "bm25": [], "lml": [], "lmjm": []}
for qid, query in query_details.items():
    query_tokenized = tokenize_query(query)
    # query_tokenized = [(tok['token']) for tok in query_tok_details['tokens']]

    score_bm25_list = {}
    doc_has_query_term = {}

    doc_to_search = doc_has_query_term.keys()
    for token_in_query in query_tokenized:
        if token_in_query not in inverted_index:
            continue
        for doc_in_tok in inverted_index[token_in_query].keys():
            doc_has_query_term[doc_in_tok] = len(inverted_index[token_in_query].keys())
            score_bm25_list[doc_in_tok] = 0


    for doc in doc_to_search:

        for token in query_tokenized:
            if token not in index_stat["term"]:
                continue

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

            score_bm25_list[doc] += bm25(tf, ld, avg_lg, tdf, tfq)

    score_bm25_list = proximity_score(inverted_index, query_tokenized, score_bm25_list)

    score_okapitf_l = []
    score_tfidf_l = []
    score_bm25_l = []
    score_lml_l = []
    score_lmjm_l = []

    for doc in doc_to_search:
        score_bm25_l.append([score_bm25_list[doc],doc,qid])

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



for key in ["bm25"]:
    query_doc_es = [str(arr[2]) + " Q0 " + arr[1] + ' ' + str(i + 1) + ' ' + str(arr[0]) + ' Exp\n' for i, arr in
                    enumerate(score[key])]

    file = open( "Results/"+ key + "_stemmed_ps_res.txt", "w+")
    file.writelines(query_doc_es)
    file.close()
