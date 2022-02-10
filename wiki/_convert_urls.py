import os

ici = os.path.dirname(__file__)

for path in os.listdir(ici):
    filePath = os.path.join(ici, path)
    print(filePath)
    fileCont = open(filePath,"r").read()
    with open(filePath,"w") as f:
        f.write(fileCont.replace("https://github.com/novitae/sterraxcyl/", "https://github.com/novitae/sterraxcyl/"))