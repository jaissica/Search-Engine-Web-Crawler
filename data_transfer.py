from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import json
from tqdm import tqdm


#1
index = 'mass_gov'
cloud_id ='9b1128ec78574fcd91ae19ac14496c8b:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRjYzY0MmMyMjQxNmQ0NzVjYmI1OTdiZmJiMjFmNTlhNCQ4ZjkxY2UzNjVlODk0NWVkYjc2YmY0NDQzZTMwMjhlNg=='
es = Elasticsearch(request_timeout =10000, cloud_id = cloud_id, http_auth = ('elastic', "rFE1RkD1dJr54MPCtHaFHqub"))

cloud_id1= 'Jaissica:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRhMThhYzg2Y2VlOGM0NjFmYjEwMDc1ZjE4OGJhNWNjNCQ0NzMyYTMwYzhiZmY0NDIzODVkZWI1YmNlYWEzZGUwMw=='
es1 = Elasticsearch(request_timeout =10000, cloud_id = cloud_id1, http_auth = ('elastic', "h28reIPsar278BCOdUAtPMS3"))



es_response = scan(
    es,
    index='mass_gov',
    query={"query": { "match_all" : {}},
           "_source" : ["inlinks", "outlinks", "author", "content"]}
)

print(es_response)

all_inlinks_outlinks = {}
for item in tqdm(es_response):
    all_inlinks_outlinks[item['_id']] = {}
    all_inlinks_outlinks[item['_id']]['inlinks'] = item['_source']['inlinks']
    all_inlinks_outlinks[item['_id']]['outlinks'] = item['_source']['outlinks']
    all_inlinks_outlinks[item['_id']]['author'] = item['_source']['author']
    all_inlinks_outlinks[item['_id']]['content'] = item['_source']['content']

with open("./stoplist.txt") as stop_f:
    stopwords = [word.strip() for word in stop_f]

body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "index.max_result_window" : 100000,
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords": stopwords
                }
            },
            "analyzer": {
                "stopped": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "content": {
                "type": "text",
                "fielddata": True,
                "analyzer": "stopped",
                "index_options": "positions"
            },
            "inlinks": {
                "type": "text"
            },
            "outlinks": {
                "type": "text"
            },
            "author": {
                "type": "text"
            }

        }
    }
}


for key in tqdm(all_inlinks_outlinks.keys()):
    doc_id = key

    es_data = {
        "content" : all_inlinks_outlinks[key]["content"],
        "inlinks" : all_inlinks_outlinks[key]["inlinks"],
        "outlinks" : all_inlinks_outlinks[key]["outlinks"],
        "author" : all_inlinks_outlinks[key]["author"],
    }

    es1.index(index='mass_gov', id = doc_id, body = es_data)