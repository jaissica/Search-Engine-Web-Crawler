import json

#Step 5(Stemmed)
f = open("./indexfiles_stemmed/doc_id_map.json")
doc_id = json.load(f)

id2doc = {}
for k, v in doc_id.items():
    id2doc[v] = k

f = open("./stemmed_words_id_dict.json")
word_id = json.load(f)

id2word = {}
for k,v in word_id.items():
    id2word[v] = k

def str_2_list(s):
    s = s.strip().strip("[").strip("]").split(",")
    return [int(i) for i in s]

inverted_index = {}
for i in range(0,85):
    with open("./indexfiles_stemmed/index/index"+ str(i) +".csv") as f:
        index = f.readlines()
        index = [i.strip() for i in index]

    with open("./indexfiles_stemmed/catalog/catalog"+ str(i) +".csv") as f:
        cat = f.readlines()
        cat = [int(c) for c in cat]

    for i,_ in enumerate(cat):
        doc_ind = index[i]
        # print(id2word[84661])
        word = id2word[int(cat[i])]

        doc_ind_dict = {}
        doc_ind = doc_ind.split("],")

        for di in doc_ind:
            # print(di)
            doc = id2doc[int(di.split(":")[0])]
            doc_ind_dict[doc] = str_2_list(di.split(":")[1])

        if word in inverted_index:
            inverted_index[word].update(doc_ind_dict)
        else:
            inverted_index[word] = doc_ind_dict


save_file = open("inverted_index_stemmed.json", "w")
json.dump(inverted_index, save_file, indent = 6)
save_file.close()




