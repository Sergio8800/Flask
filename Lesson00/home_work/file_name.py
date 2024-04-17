import random
import os


def generate_random_name():
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    random_name = ''
    for i in range(10):
        random_name += random.choice(characters)
    return random_name


def rename_file(file_path):
    new_name = generate_random_name()
    directory = os.path.dirname(file_path)
    new_file_path = os.path.join(directory, new_name)
    os.rename(file_path, new_file_path)
    return new_file_path

str = "/media/icyb342r/cats-protection_master-logo_purple_rgb-110.png"
str2 = "https://www.cats.org.uk"
st = str2 + "/" + str
print(st)