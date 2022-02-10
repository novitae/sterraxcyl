# Sterraxyl Changelog - https://github.com/novitae/sterraxcyl
## 2.3 $ ???. ? 2??? - ???
- Adding the argument `--auto_launckback` to launch back automatically after each blocking, conservating the username list (i don't know if this has a real utility for now).
## 2.2 $ Feb. 10 2022 - Rebuilt in a more Pythonic way
Since i learned a lot of more advanced python things in two months, i rebuilt sterra (again) because its architecture was completely fucked up, i don't even know how it was still working without issues ... . So i used things i discovered such as `*args` and `**kwargs`, prebuilt function for classes such as `__str__` or `__call__`, `getattr()`, `globals()`, custom Exceptions, `self.func()`, etc
### Arguments
- Added the argument `--only-usernames` in export module to export only usernames (doesn't scrape the informations about them)
- Simplified the exports and path system; at each export, the history saves the path and creates an id for the path (based on the timestamp). This id is then used to get the file, instead of the long path (the long path is still working). Also improved the History module, that can show the path of an id, and vice versa.
- Added the argument `-p|--part` in export module that is mutually exclusive with `-t|--target`, to fill the path of the part that we want to continue to export. The mutual exclusion is because the part is stored in the history, and the target list is stored in it. This change removes the error of target list when taking back the export of a part.
- Added the `interests` to `--analysis-type` in analyse module, that will show the accounts that have the most chances of being interests of the user.
- Added `--raw-raising` to the base parser, that raises the Exceptions instead of priting their name and what's going on. Useful for devellopement and debug purpose.
- Added `--clear-parts` to history module, to delete all the part stored in the module directory, and `--file-id` to get the path of a file from its export id.
- Added a `--name` option for every module that can export a file. This allows to choose the custom name of the file.
- Added `--compare-tree` that shows all the tree that leads to the compared file (to see what have been compared to what)

### Architecture
- Turned all the many parsers that was launched by a choice checking sys.argv in one single parser with the `ArgumentParser().add_subparsers()` function.
- Exceptions are now real exceptions, that can be raised if you use the new argument `--raw-raising`
- Outputs are now centralized in one function called for every print (but tqdm), so it is easier for the program to control colors, logos, etc.
- Now checking if you have access to the account if it is in private.
- Created a file that contains useful functions and definitions, to centralize these things and make it easier to change.
- The function to makes names for the files to export have now a module to do that (extrarra) since it was causing a lot of trouble.
### Details
- Instagram id now exported under str (it was exported under int before and was complicating the values conversion of dicts)
- Made a big work on the file names. To know what data was in before, it was based on regex trying to find match the name splited. Now it is working with a clear spliting and a defined letters indicating values. That makes the files and path more efficient and customizable.
- Now, if during data extraction an username responds 404, instead of skipping adding it and causing the export of a path, adding it to the result with None for each keys except for username.
- Removed the printing of the username of the account you're using in export module because it was indiscreet if you want to take a screenshot.
- If the `--name` is already taken, the program will ask for another until it is a not used one.
- It is now possible to compare list exported from compare module.

## 2.1 $ Dec. 2 2021 - New functions
- Splitted the program that was in a single file in many files to make the devellopment usage easier.
- Splitted the functions of the program in submodules; export, analyse, compare, history and convert
- Added the --part argument in export submodule:\
if the extraction get blocked at a moment, by selecting "exporting as a part", and then filling thesame command as before but with arg --part "the path given", it will export only the remaining username that haven't been extracted before.
- Added a wiki.
- Added the compare submodule,
- The history submodule,
- The convert submodule.

## 2.0 $ Nov. 11 2021 - Rebuilt
- Removed instaLoader from the module. It was used to retrieve followers and following of the target account.\
now the program makes by itself the requests to the api to retrieve followers and following.
- Removed the file storing credentials, replacing it by a sessionid or username and password function.
- Now checking if target account exists.
- Checking ssid validity.
- Placed the exporting module inside the core file to avoid any errors of package import.
- Built the core script as a python module, to be able to:
	- scrape followers and following of an account
	- retrieve the sessionid of an account with its username and password
- Added a function to see probabilities for accounts of being personnal accounts
- Added the by userid user target.
- Now asking what to do if the program gets blocked but stores already a lot of extracted informations.

## 1.3 $ Oct. 6 2021 - Faster
- Added express mode that goes ~ 15 times faster than normal requests\
(limited to 200 usernames in list to avoid a scraping blocking on the account used)
- Changed the requests logo and the starting presentation
- Moved the exportation function to an external module
- Improved error messages
- Changed the instruction list to a dict (wich is now global)
- Change the argparse help menu to a better arguments organization display
- Placed the default export directory in the module directory
- Placed the credential storing directory in the module directory

## 1.2 $ Oct. 1 2021 - CSV
- Now possible to change the export format
- Added -c & --csv function to change the export format to csv

## 1.1 $ Sep. 29 2021 - Adjustements
- Added the long description to PyPI
- Changed little colored logo for "extracting following list ..." python logo
- Added error message for if instagram detect spamming
- Removed "fbid" from the key to export because nobody knows what it is for (not a Facebook id)
- Added a waiting message during long extracting telling to the user to do something else

## 1.0 $ Sep. 28 2021 - Release of the program