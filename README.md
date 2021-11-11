# S T E R R A
## 🔭 A SOCMINT tool to get infos from an Instagram acc via its Followers / Following
### Allows you to analyse someone's followers, following, and mutuals, with these functions:
- 📊 __A probability function to determine the close social circle of your target__,
- 📥 __Export of the followers / following lists (with their details) to excel and csv,__
- ℹ️ __More informations [here](https://github.com/novitae/sterraxcyl/blob/main/README.md#-notes).__  
  
_Sterra have been recently updated, with a lot of new features, but have not been tested on every systems. Everything works, but not handled bugs or errors could happen. If it happen to you, please report it to the Issues section. Thanks :)_
### ♻️ Also a great alternative to [Export List of Followers from Instagram](https://chrome-stats.com/d/hcdbfckhdcpepllecbkaaojfgipnpbpb), that has been killed.  
## Here is the result for the accounts followed by [Mark Zuckerberg](https://www.instagram.com/zuck/), then for [Kylie Jenner](https://www.instagram.com/kyliejenner/) :
![](https://i.imgur.com/UYjVzLF.png)
![](https://i.imgur.com/XV6GKiz.png)
## 📥 Installation
- Via __PyPI__  
```
pip install sterraxcyl
```  
  
- Via __GitHub__  
```
git clone https://github.com/novitae/sterraxcyl
cd sterraxcyl
python setup.py install
```  

# 🛠 Usage:
### Check [Examples](https://github.com/novitae/sterraxcyl/blob/main/README.md#-examples) if you are lost
## 🧮 Arguments:
```python
sterra -t {followers,following,both,mutuals} (-u U | -id ID) (-lcrd U P | -ssid S)
       [--all-infos] [--do-not-export] [-e] [-f {excel,csv}] [-h] [--no-limit] [--no-btc]
       [-p P] [-a] [--pctg PCTG] [--size SIZE] [--url] [--descending]
```
### ⚠️ Required:
```python
-t {followers,following,both,mutuals}, --target {followers,following,both,mutuals}
                      what do you want to export ("followers", "following", "both" or "mutuals")
                      #mutuals are the accounts following and followed by the target
-u U, --username U    the instagram username of the aimed account
-id ID                the instagram id of the aimed account
```
### 🏠 Login:
```python
-lcrd U P, --login-credentials U P
                      login by credentials: USERNAME PASSWORD (be sure to keep a space between them)
-ssid S, --login-session-id S
                      login by SessionID
```
### 📊 Probabilities:
```python
-a, --activate-data-analysis
                      activates a data analysis that prints, for each accounts in the target lists, the probabilities of being an account from the close circle of the target
--pctg PCTG           percentage under wich we won't print results (between 0 and 98)
--size SIZE           size of the most probable username list (will be by default the size of the followers/mutuals/following list filled in)
--url                 instead of printing username, printing the url to the account
--descending          instead of printing by highest probability, printing by lowest probability
```
### ❇️ Optional:
```python
--all-infos           writes down the account extra informations that the program originaly ignores
--do-not-export       do not export to file
-e, --express         sends ultra fast requests to get the table faster (deactivated if more than 109 total usernames to avoid blocking)
-f {excel,csv}, --format {excel,csv}
                      format of the export, by default "excel"
-h, --help            show this help message and exit
--no-limit            disable the limitation for lists over 1000 follow(ers|ing); all errors you could get by doing this will not recieve help if you submit it at the issue page of sterraxcyl
--no-btc              hides the invitation to donations printed at the end
-p P, --path P        directory path where export the files (by default in your module path)
```
## 💡 Examples
#### ✅ `sterra` or `sterraxcyl` can be both used to invoke the program.  
➡️ Print the __help__:
```
sterra -h
```
⬇️ Export to __excel__, in the /export directory of the module, the __accounts kyliejenner follows__:  
```
sterra -u kyliejenner -t following -lcrd USERNAME PASSWORD
```
⬇️ Same than before, but in __express mode__, and with a lot __more details__ exported (see further will --all-infos) in a __csv__ instea of excel:
```
sterra -u kyliejenner -t following -ssid SESSIONID -e -f csv --all-infos
```
⬇️ __No exports__, but will print the __10 highest probabilities__ for each account following chrstianpedroza that he follows back of __being a personnal accounts__:
```
sterra -u chrstianpedroza -t mutuals -ssid -a --size 10 --do-not-export
```
⬇️ __Export at desktop/OSINT/ followers and following__ of chrstianpedroza, and also print the __15 lowest probabilites of being personnal accounts__ in each lists.
```
sterra -u chrstianpedroza -t both -ssid -a -p desktop/OSINT/ --descending --size 15
```
# 📌 Notes
- [Here](https://skylens.io/blog/how-to-find-your-instagram-session-id) is a tutorial on how you can find your "__sessionid__".
- If you want to extract lists __without express mode__, __it will take a long time__. I advise to do something else while the program does the job.
- If your password contains special characters (and it should...) such as "!", you may enclose it between quotes.
- Even if instagram never blocked an account used by sterra (from all the test i made, and for the people who tested for me), __it is better if you use an account made specially for the occasion__. __I do not recommend using your personnal account__ !
- The account you will use must have __2FA disabled__.
- If the target __account is private__, __you must be following it__ to extract data of it.
- If instagram blocks you, i recommend __using another account__.
- This program can be very powerful against most of instagram users, including big accounts: i tried it once one real account (with 250k followers), and it brought me very far. __I'm not responsible of its misuse, but don't do shit with it__.
- The program __doesn't work on GitPod__.
## 📇 What is exported ?
| ID | Username | FullName | Page Link | Biography | IsPrivate | Followers Count |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| __Following Count__ | __Posts Count__ | __External Link__ | __IsBusiness__ | __IsProfessional__ | __IsVerified__ |
#### With `--all-infos`:
| Upper informations | Business Adress | Business Category | Business Contact Method | Business Email | Business Phone Number | Connected Facebook Page |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| __Mutual Followed By Count__ | __Has Effects__ | __Has Channel__ | __Has Clips__ | __Has Guide__ | __Hide Like and View Count__ | __Has joined Recently__ |

## ➕ More
This program took me a lot of time; if you appreciate it, feel free to reward my work here:  
`BTC bc1qjdw2hsspdlw7j9j9qn24gnujnk5thdmt6h2kjh`  
If you believe as me that this program have a big potential, and want to work on it with me, my dms are open on twitter. 
  
I will soon have no more time for coding during a certain period. Feel free to work on my program if you want to make it better.  
If you want to help this project, here is a "to do" list:
- Exportation on tables of the probabilities printed at the end with `-a` arg.
- Adding probabilities of interests (actually there's just probabilities of being a personnal accounts)
- Making a list of rotating userangents to be less visible by instagram
- Making a timeout arg to avoid blocking (in class retrieve_list_username_infos)
- Tor ?
