import glob,os
from PIL import Image

image_paths = "train_data/rec/dicguide_29820_word_60000"

images = glob.glob(os.path.join(image_paths, "*"))

index = 0
while index < len(images):
    image_path = os.path.dirname(images[index])
    image_root = images[index][:-4]
    if ".png" in str(images[index]):
        image = Image.open(images[index])
        image = image.convert("RGB")
        image_npath = ".".join([image_root,"jpg"])
        image.save(image_npath)
        os.remove(images[index])
    index += 1