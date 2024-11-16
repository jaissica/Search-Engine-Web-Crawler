from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json


class MyEs:

    def __init__(self, text, spam, split):
        self.text = text
        self.spam = spam
        self.split = split
        self.es = Elasticsearch("http://localhost:9200", timeout=1000)
        self.term_vectors = {}
        self.spam_words = []
        self.features = {}

    def upload_es(self):
        # self.es.indices.put_template(name="hw7",
        #                              body={
        #                                  "index_patterns": "email",
        #                                  "mappings": {
        #                                      "properties": {
        #                                          "id": {
        #                                              "type": "keyword"
        #                                          },
        #                                          "text": {
        #                                              "type": "text"
        #                                          },
        #                                          "split": {
        #                                              "type": "keyword"
        #                                          },
        #                                          "spam": {
        #                                              "type": "keyword"
        #                                          }
        #                                      }
        #                                  }
        #                              })
        try:
            self.es.indices.delete(index="email")
        except:
            pass
        self.es.indices.create(index="email")
        actions = [
            {
                "_index": "email",
                "_id": i[7:],
                "_source": {
                    "id": i,
                    "text": self.text[i],
                    "spam": self.spam[i],
                    "split": self.split[i]
                }
            }
            for i in self.spam
        ]
        helpers.bulk(self.es, actions=actions)

    def get_term_vectors(self, ids):
        res = self.es.mtermvectors(index="email", body={"ids": ids}, fields=["id", "text"],
                                   field_statistics=False,
                                   payloads=False,
                                   offsets=False,
                                   positions=False)
        term_vectors = {}
        print("res",res["docs"])
        for item in res["docs"]:
            id = "".join(item["term_vectors"]["id"]['terms'].keys())
            if "text" in item["term_vectors"]:
                term_vector = item["term_vectors"]["text"]["terms"]
                term_vectors[id] = term_vector
            else:
                print(id)
                continue
        with open("./term_vectors.json", "w") as f:
            json.dump(term_vectors, f)


    def read_term_vectors(self):
        with open("./term_vectors.json", "r") as f:
            self.term_vectors = json.load(f)
        print("term vectors: done")

    def read_spam_words(self):
        with open("./my_spam_words.txt", "r") as f:
            temp = f.read().split(" ")
            temp = [i.lower() for i in temp]
            self.spam_words = temp
        print("spam words: done")

    def get_features(self):
        for word in self.spam_words:
            target_ids = helpers.scan(self.es, index="email",
                                      query={
                                          "query": {"match": {"text": word}},
                                          "_source": "id"
                                      })
            target_ids = [i["_source"]["id"] for i in target_ids]
            for id in target_ids:
                count = self.term_vectors[id][word]["term_freq"]
                if word in self.features:
                    self.features[word][id] = count
                else:
                    self.features[word] = {}
                    self.features[word][id] = count

# elastic=MyEs()
# upload_es

