import json
import os

output = ""
files_list = os.listdir("./convert")

for z in files_list:

    with open("./convert/" + z, encoding="utf-8") as j:
        x = j.read()

    y = json.loads(x)

    for i in y:

        if i["anime"]["romaji"] == i["anime"]["english"]:
            i["anime"]["english"] = ""

        output += "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t\t{}\t\t{}\t\t\t\t".format(i["anime"]["romaji"], i["anime"]["english"], i["difficulty"], i["name"], i["artist"], i["type"], i["vintage"], i["animeType"][0].upper() + i["animeType"][1:], ', '.join(i["genre"]), i["startSample"])

        if "720" in i["urls"]["catbox"].keys():
            output += "https://naedist.animemusicquiz.com/{}\t".format(i["urls"]["catbox"]["720"])
        elif "480" in i["urls"]["catbox"].keys():
            output += "https://naedist.animemusicquiz.com/{}\t".format(i["urls"]["catbox"]["480"])

        if "0" in i["urls"]["catbox"].keys():
            output += "https://naedist.animemusicquiz.com/{}\t".format(i["urls"]["catbox"]["0"])
        else:
            output += "\t"

        if i["siteIds"]["aniListId"] != "None":
            output += "{}\t{}\t{}\t{}\n".format("https://myanimelist.net/anime/" + str(i["siteIds"]["malId"]), "https://anilist.co/anime/" + str(i["siteIds"]["aniListId"]), "https://www.animenewsnetwork.com/encyclopedia/anime.php?id=" + str(i["siteIds"]["annId"]), i["altAnswers"])
        else:
            output += "{}\t\t\t{}\t{}\n".format("https://myanimelist.net/anime/" + str(i["siteIds"]["malId"]), "https://www.animenewsnetwork.com/encyclopedia/anime.php?id=" + str(i["siteIds"]["annId"]), i["altAnswers"])

with open("000output.txt", "w", encoding="utf-8") as k:
    k.write(output)

print("Complete.")
input()
