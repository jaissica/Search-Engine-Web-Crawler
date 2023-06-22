import json
from elasticsearch import Elasticsearch
from tqdm import tqdm

es = Elasticsearch()


#Step4 fetching index stats


f = open("./parsed_data.json")
docs = list(json.load(f).keys())
#print(docs)
index_stats = {"stat": {}, "doc": {}, "term": {}}

index_data = {}


tot_terms_doc = 0
terms = set()


for doc in tqdm(docs):
    tv = es.termvectors(index="ap_dataset", id=doc, body={
        "fields": ["text"],
        "offsets": "false",
        "payloads": "false",
        "positions": "false",
        "term_statistics": "true",
        "field_statistics": "true"
    })
    index_data[doc] = tv
    #print(tv)
    if "text" not in tv['term_vectors']:
        continue
    term_vectors = tv['term_vectors']['text']['terms']

    tot_tf = 0
    for term in term_vectors.keys():
        tot_tf += term_vectors[term]['term_freq']
        terms.add(term)
        index_stats["term"][term] = {"ttf": 0, "dtf": 0}
        index_stats["term"][term]["ttf"] = term_vectors[term]['ttf']
        index_stats["term"][term]["dtf"] = term_vectors[term]['doc_freq']

    tot_terms_doc += tot_tf
    #print(tot_terms_doc)
    index_stats['doc'][doc] = tot_tf

print(tot_terms_doc)
index_stats['stat']['avg_doc_length'] = tot_terms_doc / 84678
index_stats['stat']['tot_num_words'] = len(terms)

save_file = open("es_ind_stat.json", "w")
json.dump(index_stats, save_file, indent=6)
save_file.close()

save_file = open("es_ind_data.json", "w")
json.dump(index_data, save_file, indent=6)
save_file.close()