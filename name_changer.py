
import time
import glob
import shutil
import os
from pathlib import Path
from tkinter import filedialog
from lxml import html
import requests
import re

fo = open('log.txt', 'a', encoding='utf-8')
fo.close()
fo = open('log.txt', 'w', encoding='utf-8')
path = filedialog.askdirectory()
pattern = re.compile("^RJ\d{6}$") #ensure path name is exactly RJ######
files = glob.glob(path + "\\*")
for file in files:
    if os.path.isdir(file):
        rj_idx = file.rfind('\\')
        rj_code = file[rj_idx+1:]
        if pattern.match(rj_code):
            print('Processing: ' + rj_code)
            page = requests.get('http://www.dlsite.com/maniax/work/=/product_id/' + rj_code)
            tree = html.fromstring(page.content)
            title = tree.xpath('//a[@itemprop="url"]/text()')[0]
            circle = tree.xpath('//span[@itemprop="brand" and @class="maker_name"]/*/text()')[0]
            if title and circle:
                new_name = ' [' + circle + '] ' title
                try:
                    os.rename(file, os.path.join(file[:rj_idx+1], rj_code + new_name))
                except:
                    print('\t renaming error.')
                    fo.write(rj_code + ' ' + new_name + '\n')
                    #log detailed information to file
            else:
                print('\t analyzing error.')
            time.sleep(0.3) #set delay to avoid being blocked from server
fo.close()
print("Finished.")
