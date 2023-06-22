import json
import os


#Step 4(unstemmed): Inverted Index Files
f = open("unstemmed_tokens.json","r")
tokens = json.load(f)

f = open("unstemmed_words_id_dict.json","r")
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
    # print(token_docs)
    index_ind = {}
    for token in token_docs:
        # print(token)
        word_org = id_2_word[token[0]]
        word = int(token[0])
        if token[1] not in doc_int_id_dict:
            doc_int_id_dict[token[1]] = doc_int_id
            doc_int_id+=1

        doc_id = doc_int_id_dict[token[1]]
        doc_id_org = token[1]

        ind = token[2]
        # print(doc_id)
        # exit()
        # break
        if int(word) not in index:
            index[int(word)] = {doc_id : [ind]}
        elif doc_id not in index[word]:
            index[int(word)][doc_id] = [ind]
        else:
            # index[int(word)][doc_id]["tf"] += 1
            index[int(word)][doc_id].append(ind)

        if word_org not in index_org:
            index_org[word_org] = {doc_id_org : [ind]}
        elif doc_id_org not in index_org[word_org]:
            index_org[word_org][doc_id_org] = [ind]
        else:
            # index[int(word)][doc_id]["tf"] += 1
            index_org[word_org][doc_id_org].append(ind)


        if int(word) not in index_ind:
            index_ind[int(word)] = {doc_id : [ind]}
        elif doc_id not in index_ind[word]:
            index_ind[int(word)][doc_id] = [ind]
        else:
            # index[int(word)][doc_id]["tf"] += 1
            index_ind[int(word)][doc_id].append(ind)


    with open("./indexfiles_unstemmed/index/index"+ str(i) +".csv","w") as index_file:
        with open("./indexfiles_unstemmed/catalog/catalog"+ str(i) +".csv","w") as cat_file:
            for key, val in index_ind.items():
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

start_offset = 0


with open("./indexfiles_unstemmed/index.csv","w") as index_file:
    with open("./indexfiles_unstemmed/catalog.csv","w") as cat_file:
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

save_file = open("indexfiles_unstemmed/doc_id_map.json", "w")
json.dump(doc_int_id_dict, save_file, indent = 6)
save_file.close()

with open('./indexfiles_unstemmed/index.csv', 'rb') as f_in:
    data = f_in.read()

bindata = bytearray(data)



os.system('gzip --keep ./indexfiles_unstemmed/index.csv')
os.system('gzip --keep ./indexfiles_unstemmed/catalog.csv')







