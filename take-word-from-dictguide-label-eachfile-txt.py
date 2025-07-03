from os import path, makedirs
from uuid import uuid4
from PIL import Image
import argparse, cv2, json, glob


def preprocess():
    parser = argparse.ArgumentParser(description='Detector with paddleocr knowledge for image datasets')
    parser.add_argument('-c','--config', default="configs/createdataset/take-word-from-dictguide-label.json", help='take word from dictguide config file')
    parser.add_argument('-it', '--inputimagetype',default= 'jpg', help='input image type file')
    parser.add_argument('-ot', '--outputimagetype', default= 'jpg', help='set watch mode')
    args = parser.parse_args()
    return args

def load_config(config_file):
    with open(config_file, encoding='utf-8') as file:
        config = json.load(file)
    return config

def crop_image(image_path,roi, OUTPUT_FOLDER, OUTPUT_IMAGE_TYPE):
    image = cv2.imread(image_path)
    image_crop = image[int(roi[1]):int(roi[3]),int(roi[0]):int(roi[2])]
    new_image_name = str(uuid4()) + "." + OUTPUT_IMAGE_TYPE
    new_image_path = path.join(OUTPUT_FOLDER,new_image_name)
    cv2.imwrite(new_image_path,image_crop)
    return new_image_name

def main():
    args = preprocess()
    config = load_config(args.config)

    makedirs(config["OUTPUT_FOLDER"], exist_ok=True)

    label_files = glob.glob(path.join(config["LABEL_FOLDER"],"*"))

    with open(config["OUTPUT_LABEL_FILE"],"w",encoding="utf-8") as output_label_file:
        for label_file in label_files:
            label_filename = path.basename(label_file)
            filename = label_filename.split(".")[0]
            image_filename =".".join([filename,args.inputimagetype])
            image_path = path.join(config["INPUT_FOLDER"],image_filename)
            with open(label_file,"r",encoding="utf-8") as f:
                labels = f.readlines()
                for label in labels:
                    label = label.strip().split(",")
                    if len(label)>9:
                        text = label[8]+","
                    else:
                        text = label[-1]
                    x_min = min(int(label[0]),int(label[2]),int(label[4]),int(label[6]))
                    x_max = max(int(label[0]),int(label[2]),int(label[4]),int(label[6]))
                    y_min = min(int(label[1]),int(label[3]),int(label[5]),int(label[7]))
                    y_max = max(int(label[1]),int(label[3]),int(label[5]),int(label[7]))
                    roi = [x_min,y_min,x_max,y_max]
                    print(image_filename)
                    new_image_name = crop_image(image_path,roi,config["OUTPUT_FOLDER"], args.outputimagetype)
                    output_label_file.write(new_image_name+"\t"+text+"\n")

if __name__ == '__main__':
    main()