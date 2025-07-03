#!/usr/bin/env python
from os import path,mkdir
import argparse, json
import random, shutil

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
        mkdir(config["output"])
        with open(config["out_label_file"], "w",encoding='utf-8') as wf:
            for gt_name in RATES.keys():
                gt_folder_path = path.join(config["output"], gt_name)
                mkdir(gt_folder_path)
                number = int(RATES[gt_name] / sum(RATES.values()) * len(lines))
                for i in range(number):
                    print(lines[counter + i])
                    img_name,text = lines[counter + i].strip().split("\t")
                    img_path = path.join(TRAINING_FOLDER,img_name)
                    out_img_path = path.join(gt_folder_path,img_name)
                    shutil.copyfile(img_path, out_img_path)
                    name_file_path = path.join(gt_name,img_name)
                    wf.write(f"{name_file_path}\t{text}\n")
                counter += number


if __name__ == '__main__':
    main()

