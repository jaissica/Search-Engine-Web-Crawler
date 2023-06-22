import os
import re
import json


# step 1 file parser

def data_parser():
    file_name = os.listdir("./ap89_collection/")
    file_name = ["./ap89_collection/" + i for i in file_name]

    # needed objects
    files = {}
    file = list()
    add_file_flag = 0

    txt = list()
    txt_item = list()
    txt_flag = 0


    for f in file_name:
        with open(f, "r") as f:
            data = f.readlines()  # Reads the data from each file
            # scan each line, identify doc start and end
            for line in data:
                line = line.strip()  # Reads data line by line from each file
                # file end
                if re.search("</DOC>", line):
                    add_file_flag = 0
                    files[data_id] = ' '.join(file)
                    file = list()
                    # print(data_id) #Returns the data Id inside the each document
                # add lines to file
                if add_file_flag == 1:
                    # id
                    if re.search("</DOCNO>", line):
                        data_id = re.sub("(<DOCNO> )|( </DOCNO>)", "", line)
                        # print(data_id) #Returns the data Id inside the each document

                    # read text chunk
                    # text end
                    if re.search("</TEXT>", line):
                        txt_flag = 0
                    if txt_flag == 1:
                        file.append(line)  # Printing each line
                        # print(file)
                    # text start
                    if re.search("<TEXT>", line):
                        if re.search("[A-Z|a-z]*[a-z]", line):
                            file.append(line[6:])
                            # print(file)
                        txt_flag = 1
                # file start
                if re.search("<DOC>", line):
                    add_file_flag = 1
    # print(files)
    return files


def data_to_file(files):
    with open("./parsed_data.json", "w") as f:
        json.dump(files, f)


files = data_parser()
data_to_file(files)