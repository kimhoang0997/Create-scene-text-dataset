#!/usr/bin/env python
from os import path
import argparse, json
import random

def preprocess():
    parser = argparse.ArgumentParser(description='Create trainning word-image dataset by dictionaries')
    parser.add_argument('-c', '--config', metavar="config-file", default="configs/createdataset/create-trainning-dataset.json", help='split trainning dataset config file')
    args = parser.parse_args()
    return args
   
def load_config(config_file):
    with open(config_file, encoding='utf-8') as file:
        config = json.load(file)
    return config

def main():
    args = preprocess()
    config = load_config(args.config)
    RATES = config["rates"]
    TRAINING_FOLDER = config["training_folder"]
    LABEL_FILE = config["label_path"]
    
    with open(LABEL_FILE, "r",encoding='utf-8') as file:
        lines = file.readlines()
        random.shuffle(lines)
        random.shuffle(lines)
        random.shuffle(lines)
        counter = 0
        for gt_name in RATES.keys():
            gt_path = path.join(TRAINING_FOLDER, gt_name)
            with open(gt_path, "w", encoding='utf-8') as gt_file:
                number = int(RATES[gt_name] / sum(RATES.values()) * len(lines))
                for i in range(number):
                    # _, text, img_id,_,_ = lines[counter + i].split("\t")
                    # img_path = ".".join([img_id,config["image_type"]])
                    print(lines[counter + i])
                    img_path,text = lines[counter + i].strip().split("\t")
                    # _, text, img_path = lines[counter + i].strip().split("\t")
                    # img_path,text = lines[counter + i].strip().split("\t")
                    gt_file.write(f"{img_path}\t{text}\n")
                counter += number


if __name__ == '__main__':
    main()

