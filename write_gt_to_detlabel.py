import re
import ast
import copy
import glob,os

input_folder = "train_data/det/labels"
output_folder = "train_data/det"

dataset = glob.glob(os.path.join(input_folder,"*"))

names = []
cache = {}
for file in dataset:
    filename = os.path.basename(file)
    number = int(filename.split('.')[0].split("_")[1])
    img_name = "im"+"%04d" % (number,) +".jpg"
    names.append(img_name)
    cache[img_name] = {"image_name":img_name}
    file="train_data/det/labels/gt_2000.txt"
    with open(file,"r",encoding="utf-8") as f:
        rois = f.readlines()
        corrs=[]
        labels=[]
        for roi in rois:
            # if "#" not in roi:
            data = roi.strip().split(",")
            corr = [[int(data[0]),int(data[1])],[int(data[2]),int(data[3])],[int(data[4]),int(data[5])],[int(data[6]),int(data[7])]]
            label = data[8]
            if label:
                if ((abs(int(data[0])-int(data[2]))>3) or (abs(int(data[1])-int(data[3]))>3)) and \
                    ((abs(int(data[0])-int(data[6]))>3) or (abs(int(data[1])-int(data[7]))>3)) and \
                    ((abs(int(data[0])-int(data[4]))>3) or (abs(int(data[1])-int(data[5]))>3)) and \
                    ((abs(int(data[2])-int(data[6]))>3) or (abs(int(data[3])-int(data[7]))>3)) and \
                    ((abs(int(data[2])-int(data[4]))>3) or (abs(int(data[3])-int(data[5]))>3)) and \
                    ((abs(int(data[6])-int(data[4]))>3) or (abs(int(data[7])-int(data[5]))>3)):
                    if "\"" in label:
                        first = label.split("\"")[0]
                        second = label.split("\"")[1]
                        label = f"{first}\\\"{second}"
                    corrs.append(corr)
                    labels.append(label)


    cache[img_name]["transcription"] = labels    
    cache[img_name]["points"] = corrs
                
def num_sort(names):
	return list(map(int, re.findall(r'\d+', names)))[0]

names.sort(key=num_sort) 
valfile_path = os.path.join(output_folder,"val_label.txt")
testfile_path = os.path.join(output_folder,"test_label.txt")
trainfile_path = os.path.join(output_folder,"train_label.txt")
valfile = open(valfile_path,"w", encoding='utf-8')
testfile = open(testfile_path,"w", encoding='utf-8')
trainfile = open(trainfile_path,"w", encoding='utf-8')
for name in names:
    line = name+'\t['
    for i in range(len(cache[name]['transcription'])):
        line = line+'{\"transcription\": \"'+cache[name]['transcription'][i]+'\", \"points\": '+ str(cache[name]['points'][i])+'}'
        # line = line+'{\"transcription\": r\"\"\"'+cache[name]['transcription'][i]+'\"\"\", \"points\": '+ str(cache[name]['points'][i])+'}'
        if i != len(cache[name]['transcription'])-1:
            line = line + ", "
    line = line+"]\n"
    number = int(name[2:6])
    print(name, number)
    if number <= 1200:
        trainfile.write(line)
    elif number > 1500:
        testfile.write(line)
    else:
        valfile.write(line)
valfile.close()
testfile.close()
trainfile.close()
