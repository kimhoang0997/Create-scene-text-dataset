import glob, os

labels_path="dataset/raw_dictguide/dictguide_2023_fix/label_train"
output = "dataset/raw_dictguide/dictguide_2023_fix/label_test/fix"

dataset = glob.glob(os.path.join(labels_path, "*"))

index = 0
while index < len(dataset):
    label_path = dataset[index]
    label_name = os.path.basename(label_path)
    output_label_path = os.path.join(output,label_name)
    with open(label_path,"r",encoding="utf-8") as f:
        lines = f.readlines()
        newlines = []
        for line in lines:
            if "#" not in line:
                newlines.append(line)
        with open(output_label_path,"w",encoding="utf-8") as ouf:
            ouf.writelines(newlines)
            ouf.close()
        index +=1
        f.close()