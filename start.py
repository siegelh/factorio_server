# https://www.factorio.com/get-download/0.16.24/headless/linux64

# usage:
# python start.py /path/to/my/save.file 0.16.20


import sys
import os
import subprocess
from tqdm import tqdm
import requests
import time

save_file_directory = sys.argv[1]
factorio_server_version = sys.argv[2]
factorio_server_name = save_file_directory.split("/")[-1].replace(".zip","")

# Argument Check 

factorio_server_build = factorio_server_version.split(".")
print("""
Downloading Factorio server version: {0}
""".format(factorio_server_version))
if len(factorio_server_build) != 3:
    raise ValueError('Unrecognized Factorio server build number. Example accepted value is "0.16.28"')

# Download server software

url = "https://www.factorio.com/get-download/{0}/headless/linux64".format(factorio_server_version)

# Streaming, so we can iterate over the response.
r = requests.get(url, stream=True)

# Total size in bytes.
total_size = int(r.headers.get('content-length', 0))/(32*1024); 

with open('./factorio_server.tar.xz', 'wb') as f:
    for data in tqdm(r.iter_content(32*1024), total=total_size, unit='B', unit_scale=True):
        f.write(data)

# unpack the server to a folder
print("""
Unpacking Factorio server...
""")
subprocess.Popen("tar xf factorio_server.tar.xz", shell=True)
print("""
Created folder "Factorio", renaming to {0}
""".format(factorio_server_name))

for i in tqdm(range(10), total=10, unit='B', unit_scale=True):
    time.sleep(1)
    
subprocess.Popen("mv ./factorio {0}".format(factorio_server_name), shell=True)

print("""
Starting Server...
""")

subprocess.Popen("./{0}/bin/x64/factorio --start-server {1} --server-settings ./standard-server-settings.json --port 10010 | tee ./{0}/server_log.txt".format(factorio_server_name, save_file_directory), shell=True)

print("""
Server Created!...
""")
