from elasticsearch import Elasticsearch
import json


#Step 3 Searching query in elasticsearch

#Config Elastic Search
es=Elasticsearch([{"host":"localhost"}],timeout=1000)


query_id = []
query = []
score= []
id =[]
index=[]


def read_query(filename,query,query_id):
    f=open(filename)
    data = json.load(f)
    list = []

    for key, value in data.items():
        c = 0
        file = open('es_default_result.txt', 'w')
        query_id.append(key)
        query.append(value)
        client = Elasticsearch()
        index = "ap_dataset"
        doc = {
            "size": 1000,
            "query": {
                "match": {"text": value
                              }
                }
            }
        resp = es.search(index=index,
                             body=doc)
        for hit in resp['hits']['hits']:

            c = c + 1
            list.append(str(key)+" Q0 "+str(hit["_id"])+" "+str(c)+" "+str(hit["_score"])+" Exp")


    file = open('es_default_result.txt', 'w')
    for item in list:
        file.write(item + "\n")
    file.close()


def main():
    read_query("queries_new.json",query,query_id)

main()