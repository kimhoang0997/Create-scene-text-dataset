import re
import ast
import copy
filename = "train_data/train_label.txt"
output = "train_data/train_label_clean.txt"
file = open(filename,"r",encoding="utf-8")
lines = file.readlines()
cache = {}
for line in lines:
    img_name, info = line.split("\t")
    elements = re.findall(r"(\{.+?\})",info)
    print(img_name)
    labels = []
    corrs = []
    for element in elements:
        label = re.findall(r"(?<=\"\"\").*(?=\"\"\"\")",element)
        corr = ast.literal_eval(re.findall(r"\"points\": (.*)}",element)[0])
        labels.append(label[0])
        corrs.append(corr)
    cache[img_name] = {"image_name":img_name}   
    cache[img_name]["transcription"] = labels    
    cache[img_name]["points"] = corrs

names = cache.keys()

for name in names:
    transcription = copy.deepcopy(cache[name]['transcription'])
    i=0

    for index,label in enumerate(transcription):
        print("real:",label)
        if r"#" in label:
            print("remove:",label)
            cache[name]['transcription'].remove(cache[name]['transcription'][index-i])
            cache[name]['points'].remove(cache[name]['points'][index-i])
            i +=1
        
    print(cache[name]['transcription'])

with open(output,"w", encoding='utf-8') as f:
    for name in names:
        line = name+'\t[ '
        for i in range(len(cache[name]['transcription'])):
            line = line+'{\"transcription\": '+cache[name]['transcription'][i]+', \"points\": '+ str(cache[name]['points'][i])+'}'
            if i != len(cache[name]['transcription'])-1:
                line = line + ","
        line = line+"]\n"
        f.write(line)