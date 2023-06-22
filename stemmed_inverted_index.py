import json
import os

#Step 4(stemmed): Inverted Index Files
f = open("stemmed_tokens.json","r")
tokens = json.load(f)


f = open("stemmed_words_id_dict.json","r")
words_id_dict = json.load(f)

id_2_word = {}
for k, v in words_id_dict.items():
    id_2_word[v] = k


doc_int_id = 1
doc_int_id_dict = {}


index_org = {}
stats = {}


index = {}
for i, token_docs in enumerate(tokens["tokens"]):
    index_ind = {}
    for token in token_docs:
        word_org = id_2_word[token[0]]
        word = int(token[0])
        if token[1] not in doc_int_id_dict:
            doc_int_id_dict[token[1]] = doc_int_id
            doc_int_id+=1

        doc_id = doc_int_id_dict[token[1]]
        doc_id_org = token[1]

        ind = token[2]
        if int(word) not in index:
            index[int(word)] = {doc_id : [ind]}
        elif doc_id not in index[word]:
            index[int(word)][doc_id] = [ind]
        else:
            index[int(word)][doc_id].append(ind)

        if word_org not in index_org:
            index_org[word_org] = {doc_id_org : [ind]}
        elif doc_id_org not in index_org[word_org]:
            index_org[word_org][doc_id_org] = [ind]
        else:
            index_org[word_org][doc_id_org].append(ind)


        if int(word) not in index_ind:
            index_ind[int(word)] = {doc_id : [ind]}
        elif doc_id not in index_ind[word]:
            index_ind[int(word)][doc_id] = [ind]
        else:
            index_ind[int(word)][doc_id].append(ind)


    with open("./indexfiles_stemmed/index/index"+ str(i) +".csv","w") as index_file:
        with open("./indexfiles_stemmed/catalog/catalog"+ str(i) +".csv","w") as cat_file:
            for key, val in index_ind.items():
                data_term = ""
                for k, v in val.items():
                    if data_term == "":
                        data_term += str(k) + ":" +str(v)
                    else:
                        data_term += ","+ str(k) + ":" +str(v)
                data_term += "\n"
                index_file.write(data_term)
                cat_file.write(str(key) + '\n')

start_offset = 0



with open("./indexfiles_stemmed/index.csv","w") as index_file:
    with open("./indexfiles_stemmed/catalog.csv","w") as cat_file:
        for key, val in index.items():
            # index_file.write(json.dumps(val))
            data_term = ""
            for k, v in val.items():
                if data_term == "":
                    data_term += str(k) + ":" +str(v)
                else:
                    data_term += ","+ str(k) + ":" +str(v)
            data_term += "\n"
            index_file.write(data_term)
            cat_file.write(str(key) + '\n')


save_file = open("indexfiles_stemmed/doc_id_map.json", "w")
json.dump(doc_int_id_dict, save_file, indent = 6)
save_file.close()

with open('./indexfiles_stemmed/index.csv', 'rb') as f_in:
    data = f_in.read()


bindata = bytearray(data)


os.system('gzip --keep ./indexfiles_stemmed/index.csv')
os.system('gzip --keep ./indexfiles_stemmed/catalog.csv')










