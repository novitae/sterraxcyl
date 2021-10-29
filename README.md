# S T E R R A X C Y L
## A python program that allows you to put in an excel/csv table followers and/or following of an aimed account, with detailed infos on them ([see further](https://github.com/novitae/sterraxcyl#what-infos-are-exported-)).
Very useful for OSINT on instagram accounts to determine a social circle of an aimed account.  
It is an alternative to [Export List of Followers from Instagram](https://chrome-stats.com/d/hcdbfckhdcpepllecbkaaojfgipnpbpb), that has been zucced.
### Here is the result for the accounts followed by instagram :
![](https://i.imgur.com/1NYgyUn.png)

# Installation
```python
#via pypi
pip install sterraxcyl

#via github
git clone https://github.com/novitae/sterraxcyl
cd sterraxcyl
python setup.py install
```
# Usage
**At the first launch, the program will ask for some valid instagram credential.**  

Simple usage :
```python
sterra -h
#sterra or sterraxcyl can be both used to invoke the program
```
![](https://i.imgur.com/rZ1qbG5.gif)  
_The time here have been edited, it takes a bit longer to retrieve all infos (in express mode)._

Detailed usage : `sterraxcyl [-a] [-c] [-d D] [-e] [-h] [-p P] -t T -u U`  
```python
required arguments:
  -t T, --target T    #what do you want to export ("followers", "following" or "both")
  -u U, --username U  #the instagram username of the aimed account

optional arguments:
  -a, --all-infos     #writes down the account extra informations that the program originaly ignores (see further)
  -c, --csv           #exports in csv format instead of excel
  -d D, --delay D     #delay in seconds between detailed infos requests
  -e, --express-mode  #sends ultra fast requests to get the table faster; deactivated if more than 200 usernames in lists
                      #  ~ 100 followers in 15 sec (vs ~ 100 followers in 2 min for normal method)
                      #  - this mode blocked me 3 instagram accounts, use it only on little lists (less than 150 accounts in the aimed list, more there are, higher you risks to get blocked are)
  -h, --help          #show help message and exit
  -p P, --path P      #directory path where export the files (by default in your module path)
 #if you have ideas of new args, feel free to send me it (contact method on my github profile))
```

**The program isn't very fast**, espacially for long lists (~ 20 min for 1000 followers).  
But it has **never been blocked by instagram servers**, the longer list extracted was of 1400 followers.  
Slowly but surely as we say. _if you get blocked, it probably comes from your account, log with another one._

# What infos are exported ?
By defaut :  
- ID
- Username
- FullName
- Page Link
- Biography
- IsPrivate
- Followers Count
- Following Count
- Posts Count
- External Link
- IsBusiness
- IsProfessional
- IsVerified. 

Using option `--all-infos` will not make additional requests, and will add all of these infos :  
- Business Adress
- Business Category
- Business Contact Method
- Business Email
- Business Phone Number
- Connected Facebook Page
- Mutual Followed By Count
- Facebook ID
- Has Effects
- Has Channel
- Has Clips
- Has Guide
- Hide Like and View Count
- Has joined Recently


# How it works ?
Since the program will ask for your instagram credentials, here is a scheme that describes how the program works so you can see where these credentials are going.
```
                                                           if the file doesn't exists, creates it,
                                                           then ask for username and password, and
      loads the credentials from "identifiants.json" --->  then loads the credentials
      /                                           |               |
sterra --> writes the args and headers         logs in with requests, then retrieve the
           in a list that follows all          session cookies, and save it for further
           the program ("instructions")        in the list "instructions"
                                                            |
                                                            |
    check what list is aimed ;      <--- logs in with instaloader module
    if both, retrieve followers
    list, then following list. --------------> excel/csv file is created, and the head of the columns written.
    if followers / following,
    retrieve the aimed list.   ---> every username of the followers / following list is put
                                    in https://www.instagram.com/{username}/channel/?__a=1,
                                    a request is sent with the cookies retrieved before,
                                    and the response is converted to json.
                                   /                                                                        
                                  /                                                                         
        the aimed infos contained in        the list is sent to the excel/csv file,
        the json are then extracted    ---> and each infos contained in the list
        and placed in a list.               are written in their specific column.
```
_don't hesistate to contact me if you have idea of things to add to this program ! discord `aet#5349` twitter `meakaaet`_
