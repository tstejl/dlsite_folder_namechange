# dlsite_folder_namechange

> A tiny script to change folder name by getting info from dlsite server.  
> Supports Japan, Taiwan, and English sites.

## Environment Dependencies: Python 3.x, lxml, requests

### Folder name requirement

* RJ######
* RT######
* RE######

## Renaming format

RJ###### ---> RJ###### [circle_name] work_name

### Example

*RJ117353 ---> RJ117353 [シロクマの嫁] 立体音響♪シロクマ耳かき店!(添い寝&耳かきボイス作成ツール付き!)*

## Note

* RE codes will be treated as **RJ code**, thus the names will match the names of the **Japanese site**.
* Names of the folder is case sensitive, and cannot contain any characters other than the beginning two letters and six numbers
* Illegal characters in Windows filename will be replaced with empty string
