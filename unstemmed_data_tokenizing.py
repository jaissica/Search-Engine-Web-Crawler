import json
import re

#Step3(Unstemmed): Tokenizing
f = open("data_unstemmed.json","r")
file = json.load(f)


word_id = 1
words_id_dict = {}
tokens = []
token1000 = []
doc_no = 1
doc_len = {}



for doc_id in file.keys():
    text = file[doc_id].lower()
    ind_to_del = []


    if doc_no%1000 == 0:
        tokens.append(token1000)
        token1000 = []


    text = re.findall(pattern=r"\w+(?:\.?\w)*", string=text)

    final_text = []
    for t in text:
        if t != '':
            final_text.append(t)

    doc_len[doc_id] = len(final_text)

    for ind, word in enumerate(final_text):
        if word not in words_id_dict:
            words_id_dict[word] = word_id
            word_id += 1

        token1000.append((words_id_dict[word], doc_id, ind))

    doc_no += 1

if len(token1000) != 0:
    tokens.append(token1000)


print(len(tokens))


save_file = open("unstemmed_tokens.json", "w")
json.dump({"tokens" : tokens}, save_file, indent = 6)
save_file.close()


save_file = open("unstemmed_words_id_dict.json", "w")
json.dump(words_id_dict, save_file, indent = 6)
save_file.close()


save_file = open("unstemmed_doc_len_stat.json", "w")
json.dump({"stat" : {"avg_doc_length" : sum(doc_len.values())/len(doc_len.values()),
                     "tot_num_words" : len(words_id_dict)},
           "doc" : doc_len}, save_file, indent = 6)