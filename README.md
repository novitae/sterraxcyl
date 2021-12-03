# S T E R R A
## 🔭 A SOCMINT tool to get infos from an Instagram acc via its Followers / Following
### Allows you to analyse someone's followers, following, and mutuals, with these functions:
- 📊 __A probability function to determine the close social circle of your target__,
- 📥 __Export of the followers / following lists (with their details) to excel and csv,__
- 📊 __A probbaility function to determine the close social circle of your target.__
- ℹ️ __More informations [here](https://github.com/novitae/sterraxcyl/blob/main/README.md#-notes).__  
- 💱 [__Check the WIKI__](https://github.com/novitae/sterraxcyl/wiki) for the detailed Usage.
  
_Sterra have been recently updated to 2.1, with a lot of new features, but have not been tested on every systems. Everything works, but not handled bugs or errors could happen. If it happen to you, please report it to the Issues section. Thanks :)_
### ♻️ Also a great alternative to [Export List of Followers from Instagram](https://chrome-stats.com/d/hcdbfckhdcpepllecbkaaojfgipnpbpb), that has been killed.  
## Here is the result for the accounts followed by [Mark Zuckerberg](https://www.instagram.com/zuck/), then for [Kylie Jenner](https://www.instagram.com/kyliejenner/) :
![](https://i.imgur.com/UYjVzLF.png)
![](https://i.imgur.com/XV6GKiz.png)
### 🦺 Big changes are coming soon, curently working on the wiki for this new version, because it will be much complicated to use.
## 📥 Installation
- Via __PyPI__  
```
pip install sterra
```  
  
- Via __GitHub__  
```
git clone https://github.com/novitae/sterraxcyl
cd sterraxcyl
python setup.py install
# if it fails, use via PyPI
```  

# 📌 Notes
- [Here](https://skylens.io/blog/how-to-find-your-instagram-session-id) is a tutorial on how you can find your "__sessionid__".
- If you want to extract lists __without express mode__, __it will take a long time__. I advise to do something else while the program does the job.
- If your password contains special characters (and it should...) such as "!", you may enclose it between quotes.
- __It is better if you use an account made specially for the occasion__. __I do not recommend using your personnal account__ !
- The account you will use must have __2FA disabled__.
- If the target __account is private__, __you must be following it__ to extract data of it.
- If instagram blocks you, i recommend __using another account__.
- This program can be very powerful against most of instagram users, including big accounts: i tried it once one real account (with 250k followers), and it brought me very far. __I'm not responsible of its misuse, but don't do shit with it__.
- The program __doesn't work on GitPod__.

## ➕ More
This program took me a lot of time; if you appreciate it, feel free to reward my work here:  
`BTC bc1qjdw2hsspdlw7j9j9qn24gnujnk5thdmt6h2kjh`  
  
I will soon have no more time for coding during a certain period (because im joining army). Feel free to work on my program if you want to make it better.  
If you want to help this project, here is a "to do" list:
- Adding probabilities of interests in \_pro.py file (actually there's just probabilities of being a personnal accounts)
