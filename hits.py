from elasticsearch import Elasticsearch
import random
import math
import os

#4
class RootSet:
    def __init__(self):
        self.hosts = ["https://8f91ce365e8945edb76bf4443e3028e6.us-central1.gcp.cloud.es.io:9243/"]
        self.cloud_id = "9b1128ec78574fcd91ae19ac14496c8b:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRjYzY0MmMyMjQxNmQ0NzVjYmI1OTdiZmJiMjFmNTlhNCQ4ZjkxY2UzNjVlODk0NWVkYjc2YmY0NDQzZTMwMjhlNg=="
        self.index = "mass_gov"
        self.es = Elasticsearch(request_timeout=10000, cloud_id=self.cloud_id, http_auth=('elastic', "rFE1RkD1dJr54MPCtHaFHqub"))
        self.root_set = []


    def initialize(self):
        res = self.es.search(index=self.index,
                             body={
                                  "from": 0,
                                  "size": 1000,
                                  "query": {
                                    "match": {
                                      "content": "governor"
                                    }
                                  },
                                  "_source": ""
                             })['hits']['hits']
        for item in res:
            self.root_set.append(item['_id'])



class Score:

    def __init__(self, root_set):
        self.in_links = {}
        self.outlinks = {}
        self.root_set = root_set
        self.base_set = set(root_set)
        self.limit = 20
        self.authority = {}
        self.hub = {}

        self.initialize()

    def initialize(self):
        self.read_in_links()
        self.read_outlinks()

    def update_base_set(self):
        add_out_pages = set()
        for page in self.base_set:
            if page in self.outlinks:
                out_pages = self.outlinks[page]
                if len(out_pages) <= self.limit:
                    add_out_pages.update(out_pages)
                else:
                    add_out_pages.update(random.sample(out_pages, self.limit))
        add_in_pages = set()
        for page in self.base_set:
            if page in self.in_links:
                in_pages = self.in_links[page]
                if len(in_pages) <= self.limit:
                    add_in_pages.update(in_pages)
                else:
                    add_in_pages.update(random.sample(in_pages, self.limit))
        print("outlinks: ", len(add_out_pages))
        print("in_links: ", len(add_in_pages))
        self.base_set.update(add_out_pages)
        self.base_set.update(add_in_pages)
        print("length of base set: {}".format(len(self.base_set)))


    def compute_hits(self):
        # initialize both scores
        for page in self.base_set:
            self.authority[page] = 1.0
            self.hub[page] = 1.0
        k = 0
        while k < 30:
            self.update_authority()
            self.update_hub()
            self.authority[self.root_set[0]], self.hub[self.root_set[0]]
            # print(self.authority[self.root_set[0]], self.hub[self.root_set[0]])
            k += 1

    def write_hits(self):
        if os.path.exists("hits/authority.txt"):
            os.remove("hits/authority.txt")
        if os.path.exists("hits/hub.txt"):
            os.remove("hits/hub.txt")
        autho_keys = sorted(self.authority, key=self.authority.get, reverse=True)[:500]
        hub_keys = sorted(self.hub, key=self.hub.get, reverse=True)[:500]
        with open("hits/authority.txt", "a") as f:
            for key in autho_keys:
                line = "{0}    {1}\n".format(key, self.authority[key])
                f.write(line)
        with open("hits/hub.txt", "a") as f:
            for key in hub_keys:
                line = "{0}    {1}\n".format(key, self.hub[key])
                f.write(line)

    def update_authority(self):
        norm = 0
        for page in self.base_set:
            new_authority = 0
            if page in self.in_links:
                for in_page in self.in_links[page]:
                    if in_page in self.base_set:
                        new_authority += self.hub[in_page]
                self.authority[page] = new_authority
                norm += new_authority ** 2
            else:
                self.authority[page] = 0
        norm = math.sqrt(norm)
        for page in self.base_set:
            self.authority[page] = self.authority[page] / norm


    def update_hub(self):
        norm = 0
        for page in self.base_set:
            new_hub = 0
            if page in self.outlinks:
                for out_page in self.outlinks[page]:
                    if out_page in self.base_set:
                        new_hub += self.authority[out_page]
                norm += new_hub ** 2
                self.hub[page] = new_hub
            else:
                self.hub[page] = 0
        norm = math.sqrt(norm)
        for page in self.base_set:
            self.hub[page] = self.hub[page] / norm



    def read_in_links(self):
        with open("links/inlinks.txt", "r") as f:
            for line in f.readlines():
                new_line = line.replace(" \n", "")
                new_line = new_line.replace("\n", "")
                new_line = new_line.split(" ")
                if len(new_line) == 1:
                    self.in_links[new_line[0]] = []
                else:
                    self.in_links[new_line[0]] = new_line[1:]
        print("read in_links successful")


    def read_outlinks(self):
        with open("links/outlinks.txt", "r", encoding="utf-8") as f:
            for line in f.readlines():
                new_line = line.replace(" \n", "")
                new_line = new_line.replace("\n", "")
                new_line = new_line.split(" ")
                if len(new_line) == 1:
                    self.outlinks[new_line[0]] = []
                else:
                    self.outlinks[new_line[0]] = new_line[1:]
        print("read outlinks successful")



my_root = RootSet()
my_root.initialize()
my_hits = Score(my_root.root_set)
my_hits.update_base_set()
my_hits.compute_hits()
my_hits.write_hits()
