# Sterra WIKI (v2.1)
### 🔭 A SOCMINT tool to get infos from an Instagram acc via its Followers / Following
## 🗒 Summary
- [__What is sterra ?__](https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#-what-is-sterra-)
- [__Examples of usage__](https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#-examples-of-usage)
- [__Usage__](https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#-usage)
  - [Export module](https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#export)
  - [Analyse module](https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#analyse)
  - [Compare module](https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#compare)
  - [History module](https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#history)
  - [Convert module](https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#convert)
- [__Additional notes__](https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#additional-notes)

# ❓ What is sterra ?
### It is a __new way to make SOCMINT__ on instagram accounts:  
- It allows you to __determine someone's account close circle__ via data analysis module based on informations extracted of the instagram followers / following of your target.
- It also allows you to export these lists to __excel__, __csv__ and __json__, while containing basic informations on each accounts of these lists, such as __follower and following count, posts counts, name, id, biography__ ... It is perfect to manually __analyse followers and following lists on excel__.  
- It also allows you to __compare two lists__ you previously exported to sport differences and coincidences bewteen these; typically the __common username between two lists__.
![](https://i.imgur.com/RZQnHnF.png)
# 👉 Examples of usage
## Example on a big account (Mark Zuckerberg aka [@zuck](https://www.instagram.com/zuck/) on instagram):
### At first, let's scrape he's following list:
![](https://i.imgur.com/K6ngJVL.png)
1 - The submodule i am choosing (here export, to export his list of following),  
2 - The username of my target (here zuck),  
3 - The list i want to scrape (here following),  
4 - My instagram SessionID.  
### _If the following error message happens, do the following:_
![](https://i.imgur.com/ppVRNOV.png)
#### Type `2`, to export as a part the data that have already been extracted. You should get the following message:
![](https://i.imgur.com/l5b1fER.png)
#### Copy the path, and re-enter the command from before, but add the argument `--part "PATH GIVEN"` as following:
![](https://i.imgur.com/XvBZZoe.png)
#### If the errror happens again, just retype the exact same command as before, the data exported this time will be appened to the json part file.
### At the end you should get:
![](https://i.imgur.com/o4J5qH6.png)
#### Copy the path given to you (in my case: `/usr/local/lib/python3.9/site-packages/sterra/export/zuck_following.Dec-02-2021;19-48-09.xlsx`).  
#### We're going to use it to determine the potential close social circle of Mark Zuckerberg.
![](https://i.imgur.com/96f2AmJ.png)
1 - The path,  
2 - To print url instead of usernames,  
3 - To get the list from the less to the much probable to be in personnal circle.  
![](https://i.imgur.com/iibNMRO.png)
#### Here are the 3 highest probabilities accounts:
| lilyisaboss | jaiona | jolivan |
|:-:|:-:|:-:|
| ![](https://i.imgur.com/1sKyIAu.jpg) | ![](https://i.imgur.com/mH86Naq.jpg) | ![](https://i.imgur.com/u3H3HVS.jpg) |  

They all seems very personnal.
## On little accounts:
- Analyzing the mutuals list will be more efficient,
- You can also check in the followers / following list "college", "city", "university", basic terms like this that can give an idea of the location of your target.
# 🕹 Usage
If you don't see a case looking like _(default -> ....)_, it means the argument is required.
## Sterra is divided by submodules:
- __Export__, to extract and export followers / following / mutuals (account followed by and following back your target).
- __Compare__, with two lists, compare them to check their differences or common points.
- __Analyse__, to analyse lists previously exported, to determine who is more susceptible to be in your target's close circle.
- __History__, manage your export history.
- __Convert__, to convert a list already exported to another format than its actual one.
To select your submodule, simply type its name just right after invoking sterra, e.g.:
```python
# selecting analyse submodule;
sterra analyse #arguments ...
```
## Important note on the way the program works:
The submodules others than __export__ works with the path __export__ submodules gives you. Here is an example of path:
![](https://i.imgur.com/S7gSHX7.png)
When the path is asked in the arguments, it is this one, or the other last one the program gave you. To avoid errors, i advise you to write it between commas, like this : `"/Users/.../.../someones_things.excel"`.
## Export
__Default informations exported__:  
| ID | Username | FullName | Page Link | Biography | IsPrivate | Followers Count |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| __Following Count__ | __Posts Count__ | __External Link__ | __IsBusiness__ | __IsProfessional__ | __IsVerified__ |
### Required Arguments (required)
__target account__: Your target must be an instagram username or an instagram ID;
```python
-u or --username TARGETUSERNAME
#or
-id TARGETID
```
__target list__: The list you want to export;
```python
-t or --target following or followers or both or mutuals
'''
- following will be the list of accounts your target follows,
- followers will be the list of account following your target,
- both will be these two both lists,
- mutuals will be the accounts present in both list (following your target, and followed by your target).
'''
```
### Login Arguments (required)
You will have a choice to make between login via __SessionID or Credentials__.
```python
-ssid or --login-credentials SESSIONID
#or
-lcrd or --login-session-id "USERNAME" "PASSWORD"
```
### Export (required)
__format__: The format in wich export the file (default -> "excel");
```python
-f or --format excel or csv or json
```
__all infos__: Export all infos (see the following table) (default -> False);
| Default informations | Business Adress | Business Category | Business Contact Method | Business Email | Business Phone Number | Connected Facebook Page |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| __Mutual Followed By Count__ | __Has Effects__ | __Has Channel__ | __Has Clips__ | __Has Guide__ | __Hide Like and View Count__ | __Has joined Recently__ |
```python
--all-infos
```
__path__: Path to export the file (default -> module/export directory), or  
```python
-p or --path "YOUR_DESTINATION_PATH"
```
### Speed (optional)
__speed__: The speed of the extraction of the infos on each accounts in the lists (default -> express = False, -d = 0);
```python
#fast:
-e or --express
#or safe:
-d or --delay INT
```
### Optional Arguments (optional)
__help__:
```python
-h or --help
```
__part__: If you have been blocked during the follow(ers|ing) information extraction by instagram before, and selected "2 - Export what have been exported as a part", copy the path it gave you (it should look like -> followers#289309762.json), and use it as following (default -> None);
(If your first export command target was `both` or `mutuals`, use the target of the list it was extracting when it got blocked.)  
(The is an example of its usage [here](https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#-examples-of-usage)
```python
--part "PATH_GIVEN"
```
_no limit have been removed because the program has now a system of export from parts if instagram blocks the scraping._
## Compare
__files path__: Paths to the files to analyse;
```python
-f1 or --file1 "PATH_TO_FILE_1"
-f2 or --file2 "PATH_TO_FILE_2"
```
__no print__: Doesn't print the results (default -> False);
```python
-n or --no-print
```
__url__: Instead of printing usernames, printing url to the profile (default -> False);
```python
-u or --url
```
### Compare type (at least one required to run the program)
__common usernames__: Will return the common usernames between the two lists (default > False);
```python
--common-usernames
```
__not common usernames__: Will return the usernames in f1 but not in f2 (default > False);
```python
--not-common-usernames
```
### Export (not required)
__export__: Will export the list returned (default -> False);
```python
-e or --export
```
__format__: Format of the export (default -> "excel"):
```python
-f or --format excel or csv or json
```
__path__: Location path to export the file (default -> module/export directory):
```python
-p or --path "YOUR_DESTINATION_PATH"
```
## Analyse
For analysis, the best lists to analyse is following or mutuals; they represent the interests and the mutual relation of your target. The results will be way more interesting than analysing the followers list.  
  
__path__: Path to the exported file to analyse (can be excel, csv or json);
```python
-p or --path "FILE_PATH"
```
  
__analyse type__: Type of analyse to perform on the list (default -> "personnal", the only one available for now);
```python
-a or --analyse-type personnal
```
__descending__: Will print the list from 0 to 100 instead of 100 to 0 (default -> False);
```python
-d or --descending
```
__export__: Export the returned datas (the export path will be the same as the filled file) (default -> False);
```python
-e or --export
```
__format__: The format in wich export the file (if you filled the --export argument) (default -> "excel");
```python
-f or --format excel or csv or json
```
__ignore over__: The number of followers over wich the statistics will consider 0% chances of being a personnal account (for the followers coefficient; it will impact the final result (coefficient 5), but will not define alone the final result) (default -> 10000);
```python
-i or --ignore-over INT
```
__no print__: Will not print the result (be sure you checked --export arg if you od this, otherwise it will analyse but do nothing with it) (default -> False);
```python
-n or --no-print
```
__percentage__: Integer representating the percentage under wich we won't print results (between 0 and 98) (default -> 0);
```python
--pctg INT
```
__size__: Size of the probability list (default -> size of the list);
```python
-s or --size INT
```
__url__: Instead of printing the username of the accounts, printing the url of the accounts (if --export, will not export as url) (default -> False);
```python
--url
```
## History
### To run it, you'll have to choose one of the following args:
__all__: Print all the path written in the export history (default -> False);
```python
-a or --all
```
__match__: Print the path matching with a string (default -> None);
```python
-m or --match STR
```
__clear__: Clear the history (default -> False);
```python
-c or --clear
```
## Convert
### The file will be exported to a new file under another format at the same path as the entry file.
__path__: Path of the file to convert;
```python
-p or --path "PATH_OF_THE_FILE_TO_CONVERT"
```
__format__: Format of the conversion file;
```python
-f or --format excel or csv or json
```

# ➕Additional notes
- In lists, id is more important than it seems: it allows you to locate an account if it has changed of username.
- In CSV exports, `\n` is replaced by `<breakline>`, and `,` by `<comma>`.
