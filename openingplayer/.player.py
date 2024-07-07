import os
import ast
import random
import json
from unidecode import unidecode
import gdown

cmd_replace_dict = {
    "\"" : "''",
    "&" : "^^^&",
    "|" : "^^^|",
    "<" : "^^^<",
    ">" : "^^^>"
}

servers = ["nl.catbox.video", "vhdist1.catbox.video", "ladist1.catbox.video"]
best_server = ""

def check_connection():
    server_pings = []
    print("""
          >>> Checking connection...
          
                AVG PING TO CATBOX SERVERS
                =============================""")
    for i in servers:
        try:
            server_pings.append(int(os.popen('cmd /c "ping {}"'.format(i)).read().split()[-1].strip("ms")))
        except:
            server_pings.append(9999)

        print("\t\t{} : {}ms".format(i.upper(), server_pings[-1]))
    
    return servers[server_pings.index(min(server_pings))]

def alphnum(original_string):
    return unidecode("".join(filter(str.isalnum, original_string)))

def cmd_sanitise(original_string):
    for i, j in cmd_replace_dict.items():
        original_string = original_string.replace(i, j)
    return original_string

def playsong(searchresults, selectedaudio, playvideo=False):
    print("""
    [#{}] NOW PLAYING '{}'
    ==================================
    ANNID ---- {}
    Anime ---- {}
    Type ---- {}
    Song Name ---- {}
    Artist ---- {}
    Vintage ---- {} ({})
    Difficulty --- {}%
    """.format(searchresults[selectedaudio][0], 
               searchresults[selectedaudio][-10] + ".mp3" if not playvideo else searchresults[selectedaudio][-11] + ".webm", 
               searchresults[selectedaudio][1], 
               searchresults[selectedaudio][2], 
               searchresults[selectedaudio][7], 
               searchresults[selectedaudio][5], 
               searchresults[selectedaudio][6], 
               searchresults[selectedaudio][8], 
               searchresults[selectedaudio][9], 
               searchresults[selectedaudio][4]))

    if not playvideo:
        os.system('cmd /c "mpv --force-window --no-border --force-media-title=^"{}^" --title=^"{}^" --af=loudnorm=I=-12:TP=-0.5 --osd-playing-msg="\\n${{media-title}}" --osd-playing-msg-duration=3600000 --osd-font-size=30 --osd-level=2 --osd-fractions --loop-file=no {}"'.format(
            cmd_sanitise("[#{}] {}".format(searchresults[selectedaudio][0], searchresults[selectedaudio][2])),
            cmd_sanitise("[#{}] {} OP{} - '{}' by {}".format(searchresults[selectedaudio][0], searchresults[selectedaudio][2], searchresults[selectedaudio][7].split()[1], searchresults[selectedaudio][5], searchresults[selectedaudio][6])),
            searchresults[selectedaudio][-7].replace("ladist1.catbox.video", best_server)
            ))
    else:
        os.system('cmd /c "mpv --no-border --force-media-title=^"{}^" --title=^"{}^" --af=loudnorm=I=-12:TP=-0.5 --osd-playing-msg="${{media-title}}" --osd-playing-msg-duration=3600000 --osd-font-size=30 --loop-file=no {}"'.format(
            cmd_sanitise("[#{}] {}".format(searchresults[selectedaudio][0], searchresults[selectedaudio][2])),
            cmd_sanitise("[#{}] {} OP{} - '{}' by {}".format(searchresults[selectedaudio][0], searchresults[selectedaudio][2], searchresults[selectedaudio][7].split()[1], searchresults[selectedaudio][5], searchresults[selectedaudio][6])),
            searchresults[selectedaudio][-8].replace("ladist1.catbox.video", best_server)
            ))

def containschecker(entry, tocheck, index):
    return all([i in [alphnum(x.lower()) for x in entry[index].split(", ")] for i in tocheck])
        
def rangechecker(entry, tocheck, index):
    if isinstance(tocheck[0], str):
        return (tocheck[0] == 0.0) if entry[index] in ["Unrated", "N/A"] else (tocheck[0] <= entry[index] <= tocheck[1])
    else:
        return (tocheck[0] == 0.0) if entry[index] in ["Unrated", "N/A"] else (tocheck[0] <= float(entry[index]) <= tocheck[1])

def takeFirst(elem):
    return int(elem[0])

def get_playlists():
    with open("000playlists.json", encoding="utf-8") as playlists:
        return json.loads(playlists.read())


def main_init():
    print(">>> Fetching updates...")
    try:
        gdown.download("https://drive.google.com/uc?id=1gekkdfLYKEiYe_h45MxQMjPndSv9YDAD", "000data.txt", quiet=True)
    except:
        print("[!] Download was not successful.\n")


    print(">>> Initialising song list...")
    with open("000data.txt", encoding="utf-8") as songdb:
        songlist = [r.split('\t') for r in songdb.read().split('\n')[1:]]

    print(">>> Complete: loaded {} entries\n".format(str(len(songlist))))

    print("""
    ====================
    QUICK CONTROLS
    ====================
    Space - Pause
    Q - Skip song
    Arrows - Seek
    [/] - Speed
    9/0 - Volume
    M - Mute
    Shift+L - Loop
    ====================
    """)

    global best_server
    best_server = check_connection() if input("||| Check server connections? (Y/N): ").strip().lower() == "y" else servers[0]
    print()

    return songlist


def main(songlist):

    selectedmode = input("||| Enter 'S' (search mode), 'R' (random song), 'L' (random list), or 'P' (playlist)\n||| Add 'V' to the end to play video instead of audio: ").lower().strip()
    playvideo = len(selectedmode) > 1 and selectedmode[1] == "v"

    while True:    
        if selectedmode[0] == "s":
            query = alphnum(input("\n||| Search for an anime, song, or artist: ").lower())

            print("\n\nMatches found: \n")
            results = []

            for i in songlist:
                for j in [alphnum(x.lower()) for x in [i[2], i[3], i[5], i[6]] + ast.literal_eval(i[-3])]:
                    if query in j:
                        print("[{}] {} OP{} – \"{}\" by {}".format(len(results) + 1, i[2], i[7].split()[1], i[5], i[6]))
                        results.append(i)
                        break

            if len(results) == 0:
                print("\nNo results.")
                continue
            print("\nTotal results:", len(results))

            try:
                playsong(results,(int(input("\n||| Enter the corresponding number to play song: ")) - 1) % len(results), playvideo=playvideo)
            except:
                continue

        elif selectedmode[0] == "r":
            print("\n\n>>> Picking a random song...")
            playsong([random.choice(songlist)], 0, playvideo=playvideo)

        elif selectedmode[0] == "l":
            results = []
            try:
                listfilter = dict([l.lower().split(maxsplit=1) for l in input("""

                ||| Enter filter command
                ||| Syntax: list [number of songs] [flags]
                    ||| Genre flag: -g [genres to include, separated by commas]
                    ||| Type flag: -t [type]
                    ||| Studio flag: -st [studio]
                    ||| Difficulty flag: -d [lower bound:upper bound (inclusive)]
                    ||| Vintage flag: -v [loweryear-lowerseasonnumber:upperyear-upperseasonnumber (inclusive)]
                    ||| Score flag: -sc [lower bound:upper bound (inclusive)] or -sc N/A
                
                >>> """).strip().split(" -")])

                genrefilter = [alphnum(p) for p in listfilter.get("g").replace(" ", "").split(",")] if "g" in listfilter.keys() else []
                typefilter = [alphnum(p) for p in listfilter.get("t").replace(" ", "").split(",")] if "t" in listfilter.keys() else []
                studiofilter = [alphnum(p) for p in listfilter.get("st").replace(" ", "").split(",")] if "st" in listfilter.keys() else []
                diffrange = [float(x) for x in sorted(listfilter.get("d").replace(" ", "").split(":"), key=float)] if "d" in listfilter.keys() else [0.0, 100.0]
                vintagerange = sorted(listfilter.get("v").replace(" ", "").split(":")) if "v" in listfilter.keys() else ["1000-1", "9999-4"]
                if "sc" in listfilter.keys():
                    if listfilter.get("sc") == "n/a":
                        scorerange = [0.0, 0.0]
                    else:
                        scorerange = [float(x) for x in sorted(listfilter.get("sc").replace(" ", "").split(":"), key=float)]
                else:
                    scorerange = [0.0, 10.0]

                for i in songlist:
                    filtermatch = [
                        containschecker(i, genrefilter, 11), 
                        containschecker(i, typefilter, 9), 
                        containschecker(i, studiofilter, 10), 
                        rangechecker(i, diffrange, 4), 
                        rangechecker(i, vintagerange, -2), 
                        rangechecker(i, scorerange, 12)
                    ]
            
                    if all(filtermatch):
                        results.append(i)

                if len(results) < int(listfilter.get("list")):
                    output = sorted(results, key=takeFirst)
                else:
                    random.shuffle(results)
                    output = results[0:int(listfilter.get("list"))]
                    output.sort(key=takeFirst)

                if len(output) > 0:
                    count = 1
                    print("\n\nMatches found: \n")
                    for i in output:
                        print("[{}] {} OP{} – \"{}\" by {}".format(count, i[2], i[7].split()[1], i[5], i[6]))
                        count += 1

                    try:
                        while True:
                            prompt = input("\n||| Enter the corresponding number to play song, 'R' to play all at random, or 'Q' to exit: ").lower().strip()
                            if prompt == "r":
                                output_copy = list(output)
                                random.shuffle(output_copy)
                                for i in range(0, len(output_copy)):
                                    playsong(output_copy, i, playvideo=playvideo)
                            elif prompt != "q":
                                playsong(output,(int(prompt) - 1) % len(output), playvideo=playvideo)
                            else:
                                break
                    except:
                        continue
            except:
                print("\n||| Invalid syntax or no results found.")
                continue

        elif selectedmode[0] == "p":
            playlists = get_playlists()
            print("\n\nPLAYLIST MODE (Work in Progress):")
            for i, j in playlists.items():
                print("[{}] {}".format(
                    i,
                    j["playlist_name"]
                ))
            try:
                selectedplaylist = playlists[input("\n\n||| Input the ID of the playlist to play: ").strip().lower()]
                loadedresults = []
                for i in selectedplaylist["song_ids"]:
                    for j in songlist:
                        if i == j[16]:
                            loadedresults.append(j)

                print("\n\n{}".format(selectedplaylist["playlist_name"].upper()))
                
                count = 0
                for i in loadedresults:
                    count += 1
                    print("[{}] {} OP{} – \"{}\" by {}".format(count, i[2], i[7].split()[1], i[5], i[6]))

                playlist_shuffle = input("\n\n||| Shuffle playlist? (Y/N): ").strip().lower() == "y"
                playlist_loop = input("||| Loop playlist? (Y/N): ").strip().lower() == "y"

                while True:
                    if playlist_shuffle:
                        random.shuffle(loadedresults)
                    for i in range(0, len(loadedresults)):
                        playsong(loadedresults, i, playvideo=playvideo)
                    if not playlist_loop:
                        break
            except:
                pass
        else:
            break



# Driver code
songlist = main_init()
while True:
    main(songlist)