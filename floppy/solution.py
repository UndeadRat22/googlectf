import requests
import zipfile
import os
import re

path = os.getcwd()

furl = "https://storage.googleapis.com/gctf-2018-attachments/4e69382f661878c7da8f8b6b8bf73a20acd6f04ec253020100dfedbd5083bb39"

filename = "file.zip"

def download(url, savename):
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(savename, "wb") as file:
            file.write(resp.content)
    return resp.status_code

def extract(file, path = ""):
    with zipfile.PyZipFile(file) as _zip:
        _zip.extractall(path)



def seekchop(offset, filename, savename):
    with open(filename, "rb") as file:
        file.seek(offset)
        with open(savename, "wb") as _out:
            _out.write(file.read())

if __name__ == "__main__":
    code = download(furl, filename)
    if code != 200:
        print("could not download from url ERRORCODE:{}".format(code))
        exit(-1)
    expt = path + "/extracted"
    extract(filename, expt)
    seekchop(0x2FD, expt + "/foo.ico", expt+"/_out.zip")
    extract(expt+"/_out.zip", expt)

    with open(expt+"/driver.txt") as file:
        flag = re.findall(r"CTF{.*}", file.read())[0]
        print(flag)