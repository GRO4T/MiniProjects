import requests
import json
import os
import sys

usage_msg = """ usage: python3 backup.py username [backup_dest_path]"""

if (len(sys.argv) <= 1 or sys.argv[1] == '--usage'):
    print(usage_msg)
    sys.exit()

GITHUB_URL = "https://api.github.com/users/" + sys.argv[1] + "/repos"

json_response = requests.get(GITHUB_URL).json()
l = len(json_response)

backupPath = 'backup'

if (len(sys.argv) > 2):
    backupPath = sys.argv[2]

os.system('mkdir ' + backupPath)
os.chdir(backupPath)

for i in range(0, l):
    repo_url = json_response[i]['html_url']
    os.system('git clone ' + repo_url)






