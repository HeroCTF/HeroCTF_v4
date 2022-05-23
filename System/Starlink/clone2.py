#! /usr/bin/python3

######################################################################################
# Ok you got so far.                                                                 #
# But I won't do the same mistake twice. Try reading files when I'm not ziping them. #
######################################################################################

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
    p1 = subprocess.Popen(['wget', '-r', '-l', 'inf', '--no-remove-listing', '-P', DIR, url])
    p1.wait()
else:
    print('[!] Invalid URL')