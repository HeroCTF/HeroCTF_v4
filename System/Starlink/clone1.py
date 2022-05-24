#! /usr/bin/python3
import subprocess, sys, string, os, shutil
from zipfile import ZipFile
from os.path import basename


url = sys.argv[1]

WHITELIST = string.ascii_letters + "."
DIR = "/home/zip"

def check_url(url):
    prefix = 0
    if url.startswith('http://'):
        prefix = 7
    elif url.startswith('https://'):
        prefix = 8
    else:
        return False
    for l in url[prefix:]:
        if l not in WHITELIST:
            return False
    return True


if check_url(url):
    name = basename(url)
    # Clone the site
    p1 = subprocess.Popen(['wget', '-nc', '-r', '-l', 'inf', '--no-remove-listing', '-q', '-P', '/tmp', url])
    p1.wait()
    # Create a zip file
    with ZipFile(f'/tmp/{name}.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(f"/tmp/{name}"):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
    # Move file to right folder
    shutil.move(f"/tmp/{name}.zip", f"{DIR}/{name}.zip")
    os.chmod(f"{DIR}/{name}.zip", 0o777)
    shutil.rmtree(f"/tmp/{name}")
else:
    print('[!] Invalid URL')