import xml.etree.ElementTree as xml

with open("000data.txt", encoding="utf-8") as songdb:
    songlist = [r.split('\t') for r in songdb.read().split('\n')[1:]]

animeids = []
songids = []

# For AniList: use this website
    # https://malscraper.azurewebsites.net/


root = xml.parse("./xmlfiles/" + input("Enter XML filename (with extension): ")).getroot()
for i in root:
    if i.tag == "anime":
        animeids.append(i.find("series_animedb_id").text)

# print(animeids)

for i in animeids:
    for j in songlist:
        if i == j[19][30:]:
            songids.append(j[16])

print("""
"id" : {{
      "playlist_name" : "name",
      "song_ids" : {}
}}""".format(str(songids).replace("'", "\"")))
input()