import os
import ast
import random
from unidecode import unidecode

def alphnum(original_string):
    return unidecode("".join(filter(str.isalnum, original_string)))

def playsong(searchresults, selectedaudio, songlist):

    sample = random.randint(1, 90)

    print("\n\n||| Exit the file with 'Q' when you are ready to guess.")
    os.system('cmd /c "mpv --really-quiet --start={}% --loop-file=yes {}"'.format(sample, searchresults[selectedaudio][-10] + ".mp3"))

    while True:
        raw_query = input("\n||| Enter your guess: ")
        if raw_query.upper().strip() in ["/PASS", "/P"]:
            print("\n\nThe answer was: {}".format(searchresults[selectedaudio][2].upper()))
            input("Press enter to continue.\n==========================================================================================================")
            return [True, False]
        elif raw_query.upper().strip() in ["/HINT", "/H"]:
            print()
            for i in searchresults[selectedaudio][2]:
                if i == " ":
                    print("    ", end="")
                elif random.randint(1, 6) == 6 or i in [":", "-"]:
                    print(" {} ".format(i), end="")
                else:
                    print(" _ ", end="")

            print("\n\n")
            continue
        elif raw_query.upper().strip() in ["/SONGNAME", "/SN"]:
            print("\n\nSONG NAME HINT: {}\n\n".format(searchresults[selectedaudio][5]))
            continue
        elif raw_query.upper().strip() in ["/ARTIST", "/A", "/WHO"]:
            print("\n\nARTIST HINT: {}\n\n".format(searchresults[selectedaudio][6]))
            continue
        elif raw_query.upper().strip() in ["/END", "/E"]:
            return [False, False]

        query = alphnum(raw_query.lower())

        if query == alphnum(searchresults[selectedaudio][2].lower()) or query in [alphnum(x.lower()) for x in ast.literal_eval(searchresults[selectedaudio][-3])]:
            print("\n\n\t✔ CORRECT ANSWER!! ✔")
            playercorrect = True
            print("""\t
        || {}
        || {}
        || Type --- {}
        || Song Name --- {}
        || Artist --- {}
        || Vintage ---- {} ({})
        || Difficulty --- {}%
                   
                  """.format(searchresults[selectedaudio][2].upper(),
                             "=" * min(len(searchresults[selectedaudio][2].upper()) + 7, 95),
                             searchresults[selectedaudio][7],
                             searchresults[selectedaudio][5],
                             searchresults[selectedaudio][6],
                             searchresults[selectedaudio][8], 
                             searchresults[selectedaudio][9], 
                             searchresults[selectedaudio][4]))
            
            print("Press Q to continue.\n==========================================================================================================")
            os.system('cmd /c "mpv --really-quiet --start={}% --loop-file=yes {}"'.format(sample, searchresults[selectedaudio][-10] + ".mp3"))
            break

        results = []

        for i in songlist:
            for j in [alphnum(x.lower()) for x in [i[2], i[3]] + ast.literal_eval(i[-3])]:
                if query in j:
                    results.append(i[2])
                    break

        if len(results) == 0:
            print("\nNo results.")
            continue

        results = sorted(list(set(results)))

        iter = 1
        print("\n\nSEARCH RESULTS\n----------------------------------------------------------------------------------------------------------")
        for i in results[0:50]:
            print("[{}] {}".format(iter, i))
            iter += 1
        if len(results) > 50:
            print("\n>>> Only showing the first 50 results.")
        print("----------------------------------------------------------------------------------------------------------")

        try:
            selectedanswer = int(input("\n||| Enter the corresponding number: ")) - 1
            if results[selectedanswer] == searchresults[selectedaudio][2] or results[selectedanswer] in ast.literal_eval(searchresults[selectedaudio][-3]):
                print("\n\n\t✔ CORRECT ANSWER!! ✔")
                playercorrect = True
            else:
                print("\n\n\t✘ WRONG ANSWER... ✘")
                playercorrect = False
            print("""\t
        || {}
        || {}
        || Type --- {}
        || Song Name --- {}
        || Artist --- {}
        || Vintage ---- {} ({})
        || Difficulty --- {}%
                   
                  """.format(searchresults[selectedaudio][2].upper(),
                             "=" * min(len(searchresults[selectedaudio][2].upper()) + 7, 95),
                             searchresults[selectedaudio][7],
                             searchresults[selectedaudio][5],
                             searchresults[selectedaudio][6],
                             searchresults[selectedaudio][8], 
                             searchresults[selectedaudio][9], 
                             searchresults[selectedaudio][4]))
            
            print("Press Q to continue.\n==========================================================================================================")
            os.system('cmd /c "mpv --really-quiet --start={}% --loop-file=yes {}"'.format(sample, searchresults[selectedaudio][-10] + ".mp3"))
            break
        except:
            print("\nInvalid input, try again.")
            continue
    return [True, playercorrect]
        
def containschecker(entry, tocheck, index):
    return all([i in [alphnum(x.lower()) for x in entry[index].split(", ")] for i in tocheck])
        
def rangechecker(entry, tocheck, index):
    if isinstance(tocheck[0], str):
        return (tocheck[0] == 0.0) if entry[index] in ["Unrated", "N/A"] else (tocheck[0] <= entry[index] <= tocheck[1])
    else:
        return (tocheck[0] == 0.0) if entry[index] in ["Unrated", "N/A"] else (tocheck[0] <= float(entry[index]) <= tocheck[1])

def takeFirst(elem):
    return int(elem[0])

def main_init():
    print(">>> Initialising song list...")

    with open("000data.txt", encoding="utf-8") as songdb:
        songlist = [r.split('\t') for r in songdb.read().split('\n')[1:]]

    print(">>> Complete: loaded {} entries\n".format(str(len(songlist))))
    return songlist

def main(songlist):

        count = 0
        score = 0
        selectedmode = input("||| 'R' (random song), or 'L' (filtered list): ").lower().strip()

        if selectedmode == "r":
            count += 1
            print("\n\n==========================================================================================================")
            while True:
                print("\n\n>>> QUESTION {}:".format(count))
                playerresult = playsong([random.choice(songlist)], 0, songlist)
                if not playerresult[0]:
                    break
                if playerresult[1]:
                    score += 1
                count+=1
        elif selectedmode == "l":
            count += 1

            while True:
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

                    random.shuffle(results)
                    if len(results) > int(listfilter.get("list")):
                        results = results[0:int(listfilter.get("list"))]

                    break
                except:
                    print("\n||| Invalid syntax or no results found.")
                    continue

            print("\n\n==========================================================================================================")
            for i in results:
                print("\n\n>>> QUESTION {}:".format(count))
                playerresult = playsong([i], 0, songlist)
                if not playerresult[0]:
                    break
                if playerresult[1]:
                    score += 1
                count+=1

        else:
            print("\n>>> Invalid input.\n==========================================================================================================\n\n")
            return
        print("""
              
==========================================================================================================
End of game.
                
Total songs played: {}
Total correct: {} ({}%)
==========================================================================================================
                
                
                """.format(count - 1, score, round(score / (count - 1) * 100, 2)))

# Driver code
songlist = main_init()
print("""
==========================================================================================================
                  Welcome to "WE HAVE AMQ AT HOME": THE ANIME MUSIC GUESSING GAME
==========================================================================================================
      """)

while True:
    main(songlist)