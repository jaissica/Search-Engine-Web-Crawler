import json
import jsonpickle
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import urllib.robotparser




rp = urllib.robotparser.RobotFileParser()

#Step 4
json_status_path = "status.json"



f = open(json_status_path)
parsed_state = json.load(f)
out_link_graph = jsonpickle.decode(parsed_state["out_link_graph"])
in_link_graph = jsonpickle.decode(parsed_state["in_link_graph"])


f = open("preprocess_data.json")
text_data = json.load(f)


final_data = {}
for link in text_data.keys():
    if link not in in_link_graph or link not in out_link_graph:
        continue
    d = {"inlinks" : list(in_link_graph[link]),
         "outlinks" : list(out_link_graph[link]),
         "text" : text_data[link],
         "author" : "Jaissica"}

    final_data[link] = d

print(len(final_data))
save_file = open("merged_data_saved.json", "w")
json.dump(final_data, save_file, indent = 6)
save_file.close()