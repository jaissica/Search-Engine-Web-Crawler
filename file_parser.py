from glob import glob
import json

import re


#Step 3
TAG_RE = re.compile(r'<[^>]+>')


def removing_tags(text):
    return TAG_RE.sub('', text)



doc_token_json = {}
for file_path in glob("./Data/*"):
    try:
        file = open(file_path, "r")
        data = file.readlines()
    except:
        print(file_path)
        continue

    print(file_path)

    text_flag = False
    doc_flag = False
    doc_text = ""

    i = 0
    while(i<len(data)):
        line = data[i]
        if line.strip()[:7] == "<DOCNO>":
            doc_id = line.strip()[7:-8].strip()
            print(doc_id)
            while(data[i].strip()[:6] != "</DOC>" ):
                line = data[i]
                if line.strip()[:6] == "<TEXT>":
                    print("text -- ")
                    i+=1
                    while(data[i].strip()[:7] != "</TEXT>"):
                        doc_text += data[i]
                        i+=1
                else:
                    i+=1

            else:
                doc_text = doc_text.replace('\n', " ")
                doc_text = doc_text.encode("ascii", "ignore")
                doc_text = doc_text.decode()
                doc_text = removing_tags(doc_text)
                doc_token_json[doc_id] = doc_text
                doc_text = ""

        i+=1

save_file = open("saved_data.json", "w")

json.dump(doc_token_json, save_file, indent = 6)
save_file.close()