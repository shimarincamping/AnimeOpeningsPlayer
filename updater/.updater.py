import json 
import os
import time
import ast

# Json to Excel
json_list = os.listdir("./jsonfiles/updatechecks")
excel_output = ""
for h in json_list:
    with open("./jsonfiles/updatechecks/{}".format(h), encoding="utf-8") as json_file:
        json_body = json.loads(json_file.read())
    for i in json_body:
        if "catbox" not in i["urls"].keys():
            continue
        if i["anime"]["romaji"] == i["anime"]["english"]:
            i["anime"]["english"] = ""
        excel_line = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t\t{}\t\t{}\t\t\t\t".format(i["anime"]["romaji"], i["anime"]["english"], i["difficulty"], i["name"], i["artist"], i["type"], i["vintage"], i["animeType"][0].upper() + i["animeType"][1:], ', '.join(i["genre"]), i["startSample"])
        if "720" in i["urls"]["catbox"].keys():
            excel_line += "https://naedist.animemusicquiz.com/{}\t".format(i["urls"]["catbox"]["720"])
        elif "480" in i["urls"]["catbox"].keys():
            excel_line += "https://naedist.animemusicquiz.com/{}\t".format(i["urls"]["catbox"]["480"])
        if "0" in i["urls"]["catbox"].keys():
            excel_line += "https://naedist.animemusicquiz.com/{}\t".format(i["urls"]["catbox"]["0"])
        else:
            excel_line += "\t"
        excel_line += "{}\t{}\t{}\t{}\n".format("https://myanimelist.net/anime/" + str(i["siteIds"]["malId"]), "https://anilist.co/anime/" + str(i["siteIds"]["aniListId"]), "https://www.animenewsnetwork.com/encyclopedia/anime.php?id=" + str(i["siteIds"]["annId"]), i["altAnswers"])
        excel_output += excel_line

# Data comparison and overwriting
with open("000data.txt", encoding="utf-8") as current_data_file:
    current_data = [r.split('\t') for r in current_data_file.read().split('\n')[1:]]

with open("000exceptions.txt", encoding="utf-8") as exceptions_file:
    exceptions = exceptions_file.read().strip().split('\n')

if json_list:
    checking_data = [r.split('\t') for r in excel_output.strip('\n').split('\n')]
    discrepancy = []
    checked_entries = []

    for i in checking_data:
        found_match = False
        for j in current_data:
            if j[-8] == i[-6] and j[-4] == i[-2]:
                target_index = current_data.index(j)
                if j[4] != i[2]:
                    print("   (~) Difficulty changed for entry #{} ({}): {} ----> {}".format(str(target_index+1).zfill(4), j[2], str(j[4]), str(i[2])))
                    j[4] = i[2]
                if j[2] != i[0]:
                    discrepancy.append("   [!] Discrepancy found in entry #{} ({}) - roumaji: {} ----> {}".format(str(target_index+1).zfill(4), j[2],j[2], i[0]))
                if j[3] != i[1]:
                    discrepancy.append("   [!] Discrepancy found in entry #{} ({}) - english: {} ----> {}".format(str(target_index+1).zfill(4), j[2],j[3], i[1] if i[1] != "" else "null"))
                if j[5] != i[3]:
                    discrepancy.append("   [!] Discrepancy found in entry #{} ({}) - song name: {} ----> {}".format(str(target_index+1).zfill(4), j[2],j[5], i[3]))
                if j[6] != i[4] and i[4]:
                    discrepancy.append("   [!] Discrepancy found in entry #{} ({}) - artist: {} ----> {}".format(str(target_index+1).zfill(4), j[2],j[6], i[4]))
                if set(ast.literal_eval(j[-3])) != set(ast.literal_eval(i[-1])):
                    discrepancy.append("   [!] Discrepancy found in entry #{} ({}) - alt names: {} ----> {}".format(str(target_index+1).zfill(4), j[2],j[-3], i[-1]))
                if j[8] != i[6]:
                    discrepancy.append("   [!] Discrepancy found in entry #{} ({}) - vintage: {} ----> {}".format(str(target_index+1).zfill(4), j[2],j[8], i[6]))
                if j[9] != i[7]:
                    discrepancy.append("   [!] Discrepancy found in entry #{} ({}) - anime type: {} ----> {}".format(str(target_index+1).zfill(4), j[2],j[9], i[7]))
                if j[7] != i[5]:
                    discrepancy.append("   [!] Discrepancy found in entry #{} ({}) - song type: {} ----> {}".format(str(target_index+1).zfill(4), j[2],j[7], i[5]))
                if j[11] != i[9] and i[9]:
                    discrepancy.append("   [!] Discrepancy found in entry #{} ({}) - genres: {} ----> {}".format(str(target_index+1).zfill(4), j[2],j[11], i[9]))
                if j[18] != i[-5] and i[-5]:
                    discrepancy.append("   [!] Discrepancy found in entry #{} ({}) - mp3: {} ----> {}".format(str(target_index+1).zfill(4), j[2],j[18], i[-5]))
                if j[20] != i[-3] and i[-3]:
                    discrepancy.append("   [!] Discrepancy found in entry #{} ({}) - anilist: {} ----> {}".format(str(target_index+1).zfill(4), j[2],j[20], i[-3]))
                found_match = True
                checked_entries.append(target_index)
                break
        if not found_match:
            discrepancy.append("   [?] Song not found in database: {} ({})".format(i[3], i[0]))
                

    # Difficulty data output
    print("\n\nNew difficulty data will be output to: 000output.txt")
    if len(discrepancy) > 0:
        discrepancy = sorted(set(discrepancy))
        print("The discrepancies below should be resolved manually:\n")
        for i in discrepancy:
            excluded = False
            for j in exceptions:
                if j in i:
                    excluded = True
                    break
            if not excluded:
                print(i)

    with open("000output.txt", "w", encoding="utf-8") as diff_output:
        for j in current_data:
            diff_output.write(j[4] + "\n")

    with open("000updatehistory.txt") as update_history:
        update_history_list = update_history.read().strip().split("\n")

    for k in checked_entries:
        update_history_list[k] = int(time.time())

    with open("000updatehistory.txt", "w", encoding="utf-8") as update_history:
        for l in update_history_list:
            update_history.write(str(l) + "\n")

            


# File checking
discrepancy = []
download_list = []

if (input("Proceed to file checking? (Y/N): ")).strip().lower() == "y":
    file_list = set([x[:-4] for x in os.listdir(".") if x.endswith(".mp3")])
    mp3_list = set([x[15] for x in current_data if x])
    print()

    for i in current_data:
        if i[15] and i[15] not in file_list:
            discrepancy.append("   [!] File not found for entry #{} ({}) - mp3: {}".format(i[0].zfill(4), i[2], i[18]))
            download_list.append(i[18].replace("naedist.animemusicquiz.com", "eudist.animemusicquiz.com"))

    if len(discrepancy) > 0:
        discrepancy = sorted(set(discrepancy))
        for i in discrepancy:
            print(i)
        input("\nPress enter to download all missing files...\n")

        for i in set(download_list):
                os.system('cmd /c "yt-dlp -x --audio-format mp3 -c -o \"%(title)s.%(ext)s\" {}"'.format(i))

        print("\n\nAll downloads complete.")
        input("Press enter to continue to file deletion...")

    discrepancy = []
    deletion_list = []

    for i in file_list:
        if i not in mp3_list:
            discrepancy.append("   [!] Unused file found - {}".format(i))
            deletion_list.append(i + ".mp3")

    if len(discrepancy) > 0:
        discrepancy = sorted(set(discrepancy))
        for i in discrepancy:
            print(i)
        input("\nPress enter to delete all unused files...")

        deletion_list = " ".join(deletion_list)
        os.system('cmd /c "del {}"'.format(deletion_list))

        print("All deletions complete.")
    

print("\n\n\nPress enter to exit.")
input()
