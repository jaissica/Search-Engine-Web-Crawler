from elasticsearch import Elasticsearch
from os.path import exists
import json


with open("./stoplist.txt") as stop_f:
    stopwords = [word.strip() for word in stop_f]


with open('merged_data_saved.json') as user_file:
    data = user_file.read()


parsed_json = json.loads(data)

json_state_path = "./indexed.json"

if not exists(json_state_path):
    visited = set()
else:
    f = open(json_state_path)
    visited = set(json.loads(f)["visited"])


def retrieving_merged_data(my_data, es_data, key):
    auth = my_data["author"]
    es_data = es_data["_source"]
    if auth in es_data["author"]:
        return
    es.delete(index = index, id = key)
    new_outlinks = set(es_data["outlinks"])
    new_inlinks = set(es_data["inlinks"])


    my_outlinks = set(my_data["outlinks"])
    my_inlinks = set(my_data["inlinks"])

    es_data["inlinks"] = list(my_inlinks.union(new_inlinks))
    es_data["outlinks"] = list(my_outlinks.union(new_outlinks))
    es_data["author"] += (", " + auth)

    return es_data



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



index = 'mass_gov'
cloud_id ='9b1128ec78574fcd91ae19ac14496c8b:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRjYzY0MmMyMjQxNmQ0NzVjYmI1OTdiZmJiMjFmNTlhNCQ4ZjkxY2UzNjVlODk0NWVkYjc2YmY0NDQzZTMwMjhlNg=='
es = Elasticsearch(request_timeout =10000, cloud_id = cloud_id, http_auth = ('elastic', "rFE1RkD1dJr54MPCtHaFHqub"))



try:
    for key in parsed_json.keys():

        try:
            text = parsed_json[key]["text"]
            inlinks = parsed_json[key]["inlinks"]
            outlinks = parsed_json[key]["outlinks"]
            author = parsed_json[key]["author"]


            es_data = {
                "content" : text,
                "inlinks" : inlinks,
                "outlinks" : outlinks,
                "author" : author
            }

            if es.exists(index=index, id=key):
                rt_data = es.get(index = index, id = key)
                md = retrieving_merged_data(es_data, rt_data, key)
                print(md)
                if md is not None:
                    es.index(index=index, id = key, body = md)

            else:
                es.index(index=index, id = key, body = es_data)

            visited.add(key)
        except Exception as e:
            print(e)
            continue


except Exception as e:
    save_file = open("indexed.json", "w")
    json.dump({"visited" : list(visited)}, save_file, indent = 6)
    save_file.close()




