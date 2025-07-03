from PIL import Image, ImageFont
from uuid import uuid4
from glob import glob
from os import path, makedirs
from test_random_aug import Random_StrAug

imgs_path = "dataset/dictguide_label/vintext_3_2024/rec_train_sum_63_126_unrec"
label_path = "dataset/dictguide_label/vintext_3_2024/rec_train_sum_63_126_unrec/label.txt"
output_folder = "dataset/dictguide_label/vintext_3_2024/rec_train_sum_63_126_unrec_aug"
output_label = "dataset/dictguide_label/vintext_3_2024/rec_train_sum_63_126_unrec_aug/label.txt"
image_type = ".jpg"
num_aug_each_image = 5

dataset = glob(path.join(imgs_path,"*.JPG"))
with open(label_path,"r",encoding="utf-8") as label_file:
     lines = label_file.readlines()
labels = {}
for line in lines:
    line = line.strip().split("\t")
    labels[line[0]]=line[1]


with open(output_label, "w", encoding='utf-8') as output_label_file:
    for img_path in dataset:
        img = Image.open(img_path)
        img_name = path.basename(img_path)
        label = labels[img_name]
        random_StrAug = Random_StrAug(using_aug_types = ['warp', 'geometry', 'blur', 'noise', 'camera', 'pattern', 'process', 'weather'],
                                    prob_list = [0.5, 0.3, 0.2, 0.1, 0.2, 0.1, 0.1, 0.1])
        for i in range(num_aug_each_image):
            new_img = random_StrAug(img)
            image_file_name = f"{uuid4()}{image_type}"
            image_file_path = path.join(output_folder, image_file_name)
            new_img.save(image_file_path)
            row = f"{image_file_name}\t{label}\n"
            output_label_file.write(row)
