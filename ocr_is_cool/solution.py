from pytesseract import image_to_string
from PIL import Image
import requests
import zipfile
import os
import re

path = os.getcwd()
filename = "file.zip"
furl = "https://storage.googleapis.com/gctf-2018-attachments/7ad5a7d71a7ac5f5056bb95dd326603e77a38f25a76a1fb7f7e6461e7d27b6a3"

def download(url, savename):
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(savename, "wb") as file:
            file.write(resp.content)
    return resp.status_code

def extract(file, path = ""):
    with zipfile.PyZipFile(file) as _zip:
        _zip.extractall(path)

def ocrimg(path):
    with Image.open(path, "r") as img:
        return image_to_string(img)

def is_upper(c):
    if (c >= ord('A')) & (c <= ord('Z')):
        return True
    return False
    
def is_lower(c):
    if (c >= ord('a')) & (c <= ord('z')):
        return True
    return False

def shift(text, step):
    output = ""
    for letter in text:
        char = ord(letter)
        if is_lower(char):
            char = ord(letter)+step
            while (char > ord("z")):
                char-=26
        if is_upper(char):
            char = ord(letter)+step
            while (char > ord("Z")):
                char-=26
        output+=chr(char)
    return output

if __name__ == "__main__":
    code = download(furl, filename)
    if code != 200:
        print("could not download from url ERRORCODE:{}".format(code))
        exit(-1)
    extract(filename, path + "/extracted")

    enc_text = ocrimg(path + "/extracted/OCR_is_cool.png")
    flag = re.findall(r"[A-Z]{3}{.*}", enc_text)[0]
    for _ in range (0, 26):
        flag = shift(flag, 1)
        if "CTF" in flag:
            break
    
    print(flag)