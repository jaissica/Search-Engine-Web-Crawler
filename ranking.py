from elasticsearch import Elasticsearch
import json

index = 'mass_gov'
hosts = ["https://umang.kb.us-central1.gcp.cloud.es.io:9243/"]
cloud_id ='Umang:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ0MTcwYmM4NzNhZWY0Y2ZhODc5NWZjMjFiNmU2YWFjMyRjNmRlMDljODE0Nzc0YTdiYjJlZTdmYjkxOTk3N2UyMg=='
es = Elasticsearch(request_timeout=10000, cloud_id=cloud_id, http_auth=('elastic', "CrX7HTtr0xUnS0KUQ8PcnQHd"))





query_id = []
query = []
score= []
id =[]


def access_query(query,query_id):
    print("query",query)
    print("query_id",query_id)
    e = 400
    d=200
    c=0
    list = []
    file = open('output_gen.txt', 'a')
    query_id=query_id
    query=query
    index = 'mass_gov'
    doc = {
            "size": 200,
            "query": {
                "match": {"content": query
                              }
                }
            }
    resp = es.search(index=index,
                             body=doc)
    print("resp",resp)
    for hit in resp['hits']['hits']:
        e = e + 1
        list.append(str(query_id)+" Q0 "+str(hit["_id"])+" "+str(e)+" "+str(hit["_score"])+" Exp")
    print(list)
    file = open('output_gen.txt', 'a')
    for item in list:
        file.write(item + "\n")
    file.close()

def main():
    query = "deval patrick election"
    query_id = 150204
    access_query(query,query_id)

main()