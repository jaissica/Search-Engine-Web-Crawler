from module.data_parser import MyParser
from module.es import MyEs
from module.part_1 import MyDf
import pandas as pd
from module.part_2 import MyDf2

my_data = MyParser()
my_data.read_html()
my_data.read_label()
my_data.read_from_local()

ids = [i for i in my_data.spam]
print(my_data.text)
print(my_data.spam)
print(my_data.split)

my_es = MyEs(my_data.text, my_data.spam, my_data.split)

my_es.upload_es()
my_es.get_term_vectors(ids)
my_es.read_term_vectors()
my_es.read_spam_words()
my_es.get_features()


#  PART 1
ids = [i for i in my_data.spam]
my_df = MyDf(ids, my_es.features, my_data.spam, my_data.split)
my_df.dt()
my_df.lr()
my_df.mnb()

# PART 2
simple_ids = [i[7:] for i in ids]
text = [my_data.text[i] for i in ids]
label = []
for i in ids:
    if my_data.spam[i] == "spam":
        label.append(1)
    else:
        label.append(0)
split = [my_data.split[i] for i in ids]
my_df = MyDf2(simple_ids, text, label, split)
my_df.dt()
my_df.mnb()
my_df.lr()
