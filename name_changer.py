
import time
import glob
import shutil
import os
from pathlib import Path
from tkinter import filedialog
from lxml import html
import requests
import re

RJ_WEBPATH = 'http://www.dlsite.com/maniax/work/=/product_id/'
RT_WEBPATH = 'https://www.dlsite.com.tw/work/product_id/'
COOKIE =  {'adultchecked': '1'}

def match_rj(rj_code):
    r = requests.get(RJ_WEBPATH + rj_code, allow_redirects=False)
    if r.status_code != 200:
        print(r.status_code, r.headers['Location'])
        return r.status_code, "", ""
    tree = html.fromstring(r.content)
    title = tree.xpath('//a[@itemprop="url"]/text()')[0]
    circle = tree.xpath('//span[@itemprop="brand" and @class="maker_name"]/*/text()')[0]
    return 200, title, circle

def match_rt(rt_code):
    r = requests.get(RT_WEBPATH + rt_code + '.html',
                    allow_redirects=False, cookies=RT_COOKIE)
    if r.status_code != 200:
        print("\tStatus code: ", r.status_code, ";\n\tRedirect to:", r.headers['Location'])
        return r.status_code, "", ""
    tree = html.fromstring(r.content)
    title = tree.xpath('//div[@class="works_summary"]/h3/text()')[0]
    circle = tree.xpath('//a[@class="summary_author"]/text()')[0]
    return 200, title, circle

path = filedialog.askdirectory()
fo = None
#ensure path name is exactly RJ###### or RT###### or RE######
pattern = re.compile("^R[EJT]\d{6}$")

files = glob.glob(path + "\\*")
for file in files:
    if os.path.isdir(file):
        r_idx = file.rfind('\\')
        r_code = file[r_idx+1:]
        if pattern.match(r_code):
            print('Processing: ' + r_code)
            if r_code[1] in ("J", "E"): #treat RE as RJ
                r_status, title, circle = match_rj(r_code)
            elif r_code[1] == "T" :
                r_status, title, circle = match_rt(r_code)
            if r_status == 200 and title and circle:
                new_name = ' [' + circle + '] ' + title
                try:
                    os.rename(file, os.path.join(file[:r_idx+1], r_code + new_name))
                except:
                    print('--Renaming error.')
                    if fo == None:
                        fo = open(path + '/log.txt', 'a', encoding='utf-8')
                        print('--A log.txt file has been created under selected directory.')
                        fo.close()
                    fo = open(path + '/log.txt', 'w', encoding='utf-8')
                    fo.write(r_code + ' ' + new_name + '\n')
                    print('--Formatted name has been saved to file.')
                    #log detailed information to file
            else:
                print('**An error occurred.')
            time.sleep(0.3) #set delay to avoid being blocked from server
fo.close()
print("~Finished.")
