
from PIL import Image, ImageFont
from uuid import uuid4
import random
from glob import glob
from os import remove, path, makedirs
import unidecode

NUMBER_OF_NAME = 1000
NUMBER_CAPITAL_NAME = 500
# NUMBER_OF_EMAIL = 100
NUMBER_OF_SPECIAL = 2000

FIRSTNAME_PATH = "dataset/name/firstname.txt"
MIDDLENAME_PATH = "dataset/name/middlename.txt"
LASTNAME_PATH = "dataset/name/lastname.txt"
SPECIAL_LIST = "dataset/dicts/special_character.txt"
DICTIONARY_PATH = "dataset/dicts/vi.txt"
FONTS_PATH = "dataset/fonts"
OUTPUT_FOLDER_PATH = "dataset/special_data"
IMAGE_TYPE = ".jpg"
LABELS_PATH = "dataset/special_data/label.txt"
fonts = glob(path.join(FONTS_PATH, "*"))
random.shuffle(fonts)
makedirs(OUTPUT_FOLDER_PATH, exist_ok=True)

def create_image(TEXT,OUTPUT_FOLDER_PATH,LABELS_PATH,IMAGE_TYPE):
    font_size = random.randint(30, 120)
    color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(25, 255)
    )
    font_path = random.choice(fonts)
    font = ImageFont.truetype(font_path, size=font_size)
    mask_image = font.getmask(TEXT, "L")
    img = Image.new("RGB", mask_image.size, color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    img.im.paste(color, (0, 0) + mask_image.size, mask_image)
    filename = str(uuid4())
    img_name = f"{filename}{IMAGE_TYPE}"
    img.save(path.join(OUTPUT_FOLDER_PATH, img_name))
    message = f"{img_name}\t{TEXT}"
    return message
        
                  

with open(FIRSTNAME_PATH, encoding='utf-8') as file:
    FIRSTNAME = file.readlines()
    random.shuffle(FIRSTNAME)

with open(MIDDLENAME_PATH, encoding='utf-8') as file:
    MIDDLENAME = file.readlines()
    random.shuffle(MIDDLENAME)

with open(DICTIONARY_PATH, encoding='utf-8') as file:
    dictionary = file.readlines()
    random.shuffle(dictionary)

LASTNAME = []
LASTNAME_RATE = []
with open(LASTNAME_PATH, encoding='utf-8') as file:
    names = file.readlines()
    for i in names:
        name = i.split()[0]
        name_weight = i.split()[1]
        LASTNAME.append(name)
        LASTNAME_RATE.append(float(name_weight))

with open(SPECIAL_LIST, encoding='utf-8') as file:
    SPECIAL = file.readlines()
    random.shuffle(SPECIAL)

## create full name
FULLNAME = []
with open(LABELS_PATH, "a", encoding='utf-8') as file:
    i = 0
    while i < NUMBER_OF_NAME:
        LASTNAME_choosen = random.choices(LASTNAME, LASTNAME_RATE)[0]
        MIDDLENAME_choosen = random.choice(MIDDLENAME).strip()
        FIRSTNAME_choosen = random.choice(FIRSTNAME).strip()
        NAME = ' '.join([LASTNAME_choosen, MIDDLENAME_choosen, FIRSTNAME_choosen])
        if i > (NUMBER_OF_NAME - NUMBER_CAPITAL_NAME):
            NAME = NAME.upper()
        FULLNAME.append(NAME)
        i+=1
        message = create_image(NAME,OUTPUT_FOLDER_PATH,LABELS_PATH,IMAGE_TYPE)
        print(f"{message}")
        file.write(f"{message}\n")


# ## create email
# EMAIL = []
# i = 0
# with open(LABELS_PATH, "a", encoding='utf-8') as file:
#     while i < NUMBER_OF_EMAIL:
#         domain_email = ['@gmail.com', '@yahoo.com', '@outlook.com', '@hotmail.com', '@icloud.com', '@mail.com', '@live.com', '@aol.com', '@yandex.com', '@protonmail.com', '@zoho.com', '@gmx.com', '@tutanota.com', '@mail.com', '@yopmail.com', '@mailinator.com', '@guerrillamail.com', '@10minutemail.com', '@dispostable.com', '@temp-mail.org', '@mailnesia.com', '@maildrop.cc', '@fakeinbox.com', '@mailcatch.com', '@mailnesia.com', '@mailinator2.com', '@mailin8r.com', '@spamgourmet.com', '@spam4.me', '@spambog.com', '@getnada.com', '@sharklasers.com', '@guerrillamail.com', '@10minutemail.com', '@temp-mail.org', '@mailnesia.com', '@maildrop.cc', '@fakeinbox.com', '@mailcatch.com', '@mailnesia.com', '@mailinator2.com', '@mailin8r.com', '@spamgourmet.com', '@spam4.me', '@spambog.com', '@getnada.com', '@sharklasers.com']
#         name_mail = random.choice(FULLNAME).replace(' ','').lower()
#         name_mail = unidecode.unidecode(name_mail)
#         mail = name_mail + random.choice(domain_email)
#         EMAIL.append(mail)
#         i+=1
#         message = create_image(mail,OUTPUT_FOLDER_PATH,LABELS_PATH,IMAGE_TYPE)
#         print(f"{message}")
#         file.write(f"{message}\n")

## create data include special character
SPECIAL_DATA = []
i = 0
with open(LABELS_PATH, "a", encoding='utf-8') as file:
    while i < NUMBER_OF_SPECIAL:
        i+=1
        word1 = random.choice(dictionary).strip()
        special = random.choice(SPECIAL).strip()
        if special == "\"":
            special_word = special+word1 + special
        elif special == "{":
            special_word = special+word1 +"}"
        elif special == "[":
            special_word = special+word1 +"]"
        elif special == "(":
            special_word = special+word1 +")"
        else:
            special_word = ' '.join([word1,special])
        SPECIAL_DATA.append(special_word)
        message = create_image(special_word,OUTPUT_FOLDER_PATH,LABELS_PATH,IMAGE_TYPE)
        print(f"{message}")
        file.write(f"{message}\n")












