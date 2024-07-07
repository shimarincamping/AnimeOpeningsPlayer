import os

with open("000data.txt", encoding="utf-8") as songdb:
    songlist = [r.split('\t') for r in songdb.read().split('\n')[1:]]

filelist = [x[:-5] for x in os.listdir(".") if x.endswith(".webm")]

for i in filelist:
    for j in songlist:
        if i == j[14] and os.path.exists(i + ".webm"):
            try:
                os.rename(i + ".webm", j[2].translate(str.maketrans('','','\\/:*?"|')) + ".webm")
            except:
                highest_number = 1
                while True:
                    if (os.path.exists(j[2].translate(str.maketrans('','','\\/:*?"|')) + " .....(" + str(highest_number) + ").webm")):
                        highest_number += 1
                    else:
                        break
                        
                os.rename(i + ".webm", j[2].translate(str.maketrans('','','\\/:*?"|')) + " .....(" + str(highest_number) + ").webm")

input()
