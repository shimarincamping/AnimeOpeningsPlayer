import os

with open("000data.txt", encoding="utf-8") as songdb:
    songlist = [r.split('\t') for r in songdb.read().split('\n')[1:]]

filelist = [x[:-4] for x in os.listdir(".") if x.endswith(".mp3")]

for i in filelist:
    for j in songlist:
        if i == j[15] and os.path.exists(i + ".mp3"):
            try:
                os.rename(i + ".mp3", j[2].translate(str.maketrans('','','\\/:*?"|')) + ".mp3")
            except:
                highest_number = 1
                while True:
                    if (os.path.exists(j[2].translate(str.maketrans('','','\\/:*?"|')) + " (" + str(highest_number) + ").mp3")):
                        highest_number += 1
                    else:
                        break
                        
                os.rename(i + ".mp3", j[2].translate(str.maketrans('','','\\/:*?"|')) + " (" + str(highest_number) + ").mp3")

input()
