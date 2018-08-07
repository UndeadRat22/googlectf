import requests
import zipfile
import os
import pdftotext
import re

furl = "https://storage.googleapis.com/gctf-2018-attachments/5a0fad5699f75dee39434cc26587411b948e0574a545ef4157e5bf4700e9d62a"
filename = "file.zip"

def gettext(filename):
    with open(filename, "rb") as file:
        pdf = pdftotext.PDF(file)
        text = ""
        for page in pdf:
            text += page
        return text

def download(url, savename):
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(savename, "wb") as file:
            file.write(resp.content)
    return resp.status_code

def extract(file, path = ""):
    _zip = zipfile.PyZipFile(file)
    _zip.extractall(path)

if __name__ == "__main__":
    download(furl, filename)
    extract(filename, path = os.getcwd() + "/extracted")
    text = gettext(os.getcwd() + "/extracted/challenge.pdf")
    flag = re.findall(r"CTF{.*}", text)[0]
    print(flag)