import os
from itertools import count
from bs4 import BeautifulSoup
import lxml
import re
from progressbar import ProgressBar, Bar, Percentage
import random
import json
import email.parser


class MyParser:

    def __init__(self):
        #self.files = listdir()
        #path = os.getcwd()
        path="./trec07p/data"
        #path="./trec07p"
        #print(os.listdir(path))
        self.files = os.listdir(path)
        print("files :",self.files)
#        print(count(self.files))
        self.spam = {}
        self.text = {}
        self.split = {}
        self.email_parser = email.parser.Parser()
    def read_html(self):
        bar = ProgressBar(widgets=["Read html: ", Bar(), Percentage()], maxval=len(self.files))
        print("length",len(self.files))
        bar.start()
        count = 0
        for p in self.files:
            print(p)
            with open("./trec07p/data/{}".format(p), "r", encoding="ISO-8859-1") as f:
            #with open("trec07p/data/"+p, "r", encoding="ISO-8859-1") as f:
                all_data = f.read()
            parsed_email = self.email_parser.parsestr(text=all_data)
            text = self.get_all_content(parsed_email)
            soup = BeautifulSoup(text, "lxml")
            # text = re.findall("\w+", soup.get_text())
            self.text[p] = soup.get_text()
            print(self.text[p])
            if random.sample([1, 1, 1, 1, 0], 1)[0]:
                self.split[p] = "train"
            else:
                self.split[p] = "test"

            count += 1
            bar.update(count)
        bar.finish()

    def read_label(self):
        with open("./trec07p/full/index", "r") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                spam, file = line.split(" ")
                file = re.findall("/\w+.\w*$", file)[0][1:]
                self.spam[file] = spam
                print("read_label",self.spam[file])


    def read_from_local(self):
        with open("./text.json", "a") as f:
            json.dump(self.text,f)
        with open("./split.json", "a") as f:
            json.dump(self.split,f)
        with open("./spam.json", "a") as f:
            json.dump(self.spam,f)
        print("text, spam, split: done")

    def get_all_content(self, e):
        if not e.is_multipart():
            return e.get_payload()
        else:
            text = ""
            for p in e.get_payload():
                text += self.get_all_content(p)
            print("text",text)
            return text

