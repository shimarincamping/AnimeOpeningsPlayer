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

servers = ["naedist.animemusicquiz.com", "nawdist.animemusicquiz.com", "eudist.animemusicquiz.com"]
best_server = ""

def check_connection():
    server_pings = []
    print("""
          >>> Checking connection...
          
                AVERAGE PING TO FILE SERVERS
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

def get_mpv_title(id, anime_name):
    return cmd_sanitise("[#{}] {}".format(id, anime_name))

def get_window_title(id, anime_name, op_number, song_name, artist_name):
    return cmd_sanitise("[#{}] {} OP{} - '{}' by {}".format(id, anime_name, op_number[8:], song_name, artist_name))

def stream_mp3(selected_audio, loudnorm_I=-12, loudnorm_TP=-0.5):
    os.system('cmd /c "mpv --force-window --no-border --force-media-title=^"{}^" --title=^"{}^" --af=loudnorm=I={}:TP={} --osd-playing-msg="\\n${{media-title}}" --osd-playing-msg-duration=3600000 --osd-font-size=30 --osd-level=2 --osd-fractions --loop-file=no {}"'.format(
        get_mpv_title(selected_audio[0], selected_audio[2]),
        get_window_title(selected_audio[0], selected_audio[2], selected_audio[7], selected_audio[5], selected_audio[6]),
        loudnorm_I, loudnorm_TP,
        selected_audio[-7].replace("naedist.animemusicquiz.com", best_server)
    ))

def stream_webm(selected_audio, loudnorm_I=-12, loudnorm_TP=-0.5):
    os.system('cmd /c "mpv --no-border --force-media-title=^"{}^" --title=^"{}^" --af=loudnorm=I={}:TP={} --osd-playing-msg="${{media-title}}" --osd-playing-msg-duration=3600000 --osd-font-size=30 --loop-file=no {}"'.format(
        get_mpv_title(selected_audio[0], selected_audio[2]),
        get_window_title(selected_audio[0], selected_audio[2], selected_audio[7], selected_audio[5], selected_audio[6]),
        loudnorm_I, loudnorm_TP,
        selected_audio[-8].replace("naedist.animemusicquiz.com", best_server)
    ))

def play_song(selected_audio):
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
    """.format(selected_audio[0], 
               selected_audio[-10] + ".mp3" if not play_video else selected_audio[-11] + ".webm", 
               selected_audio[1], 
               selected_audio[2], 
               selected_audio[7], 
               selected_audio[5], 
               selected_audio[6], 
               selected_audio[8], 
               selected_audio[9], 
               selected_audio[4]))

    if not play_video:
        stream_mp3(selected_audio)
    else:
        stream_webm(selected_audio)

def contains_checker(entry, tocheck, index):
    return all([i in [alphnum(x.lower()) for x in entry[index].split(", ")] for i in tocheck])
        
def range_checker(entry, tocheck, index):
    if isinstance(tocheck[0], str):
        return (tocheck[0] == 0.0) if entry[index] in ["Unrated", "N/A"] else (tocheck[0] <= entry[index] <= tocheck[1])
    else:
        return (tocheck[0] == 0.0) if entry[index] in ["Unrated", "N/A"] else (tocheck[0] <= float(entry[index]) <= tocheck[1])

def take_first(elem):
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
        song_list = [r.split('\t') for r in songdb.read().split('\n')[1:]]

    print(">>> Complete: loaded {} entries\n".format(str(len(song_list))))

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
    best_server = check_connection() if input("||| Check server connections? (Y/N): ").strip().lower() == "y" else servers[-1]
    print()

    return song_list


def get_search_results(query):
    results = []
    for i in song_list:
        for j in [alphnum(x.lower()) for x in [i[2], i[3], i[5], i[6]] + ast.literal_eval(i[-3])]:
            if query in j:
                print("[{}] {} OP{} – \"{}\" by {}".format(len(results) + 1, i[2], i[7][8:], i[5], i[6]))
                results.append(i)
                break
    return results


def begin_search_mode():
    query = alphnum(input("\n||| Search for an anime, song, or artist: ").lower())

    print("\n\nMatches found: \n")
    results = get_search_results(query)

    if len(results) == 0:
        print("\nNo results.")
        return
    print("\nTotal results:", len(results))

    try:
        play_song(results[(int(input("\n||| Enter the corresponding number to play song: ")) - 1) % len(results)])
    except:
        return
    

def begin_random_mode():
    print("\n\n>>> Picking a random song...")
    play_song(random.choice(song_list))


def get_filter_results(list_filter):
    genre_filter = [alphnum(p) for p in list_filter.get("g").replace(" ", "").split(",")] if "g" in list_filter.keys() else []
    type_filter = [alphnum(p) for p in list_filter.get("t").replace(" ", "").split(",")] if "t" in list_filter.keys() else []
    studio_filter = [alphnum(p) for p in list_filter.get("st").replace(" ", "").split(",")] if "st" in list_filter.keys() else []
    diff_range = [float(x) for x in sorted(list_filter.get("d").replace(" ", "").split(":"), key=float)] if "d" in list_filter.keys() else [0.0, 100.0]
    vintage_range = sorted(list_filter.get("v").replace(" ", "").split(":")) if "v" in list_filter.keys() else ["1000-1", "9999-4"]
    if "sc" in list_filter.keys():
        score_range = [0.0, 0.0] if list_filter.get("sc") == "n/a" else [float(x) for x in sorted(list_filter.get("sc").replace(" ", "").split(":"), key=float)]
    else:
        score_range = [0.0, 10.0]


    results = [i for i in song_list if all([
            contains_checker(i, genre_filter, 11), 
            contains_checker(i, type_filter, 9), 
            contains_checker(i, studio_filter, 10), 
            range_checker(i, diff_range, 4), 
            range_checker(i, vintage_range, -2), 
            range_checker(i, score_range, 12)])]
    return results


def begin_list_mode():
    try:
        list_filter = dict([l.lower().split(maxsplit=1) for l in input("""

        ||| Enter filter command
        ||| Syntax: list [number of songs] [flags]
            ||| Genre flag: -g [genres to include, separated by commas]
            ||| Type flag: -t [type]
            ||| Studio flag: -st [studio]
            ||| Difficulty flag: -d [lower bound:upper bound (inclusive)]
            ||| Vintage flag: -v [loweryear-lowerseasonnumber:upperyear-upperseasonnumber (inclusive)]
            ||| Score flag: -sc [lower bound:upper bound (inclusive)] or -sc N/A
        
        >>> """).strip().split(" -")])

        results = get_filter_results(list_filter)

        if len(results) < int(list_filter.get("list")):
            output = sorted(results, key=take_first)
        else:
            random.shuffle(results)
            output = results[0:int(list_filter.get("list"))]
            output.sort(key=take_first)

        if len(output) > 0:
            count = 1
            print("\n\nMatches found: \n")
            for i in output:
                print("[{}] {} OP{} – \"{}\" by {}".format(count, i[2], i[7][8:], i[5], i[6]))
                count += 1

            try:
                while True:
                    prompt = input("\n||| Enter the corresponding number to play song, 'R' to play all at random, or 'Q' to exit: ").lower().strip()
                    match prompt:
                        case "r":
                            output_copy = list(output)
                            random.shuffle(output_copy)
                            for i in range(0, len(output_copy)):
                                play_song(output_copy[i])
                        case "q":
                            break
                        case _:
                            play_song(output[(int(prompt) - 1) % len(output)])
            except:
                pass
    except:
        print("\n||| Invalid syntax or no results found.")
    
def begin_playlist_mode():
    playlists = get_playlists()
    print("\n\nPLAYLIST MODE (Work in Progress):")

    for i, j in playlists.items():
        print("[{}] {}".format(i, j["playlist_name"]))

    try:
        selected_playlist = playlists[input("\n\n||| Input the ID of the playlist to play: ").strip().lower()]
        loaded_results = []
        for i in selected_playlist["song_ids"]:
            for j in song_list:
                if i == j[16]:
                    loaded_results.append(j)

        print("\n\n{}".format(selected_playlist["playlist_name"].upper()))
        
        count = 0
        for i in loaded_results:
            count += 1
            print("[{}] {} OP{} – \"{}\" by {}".format(count, i[2], i[7][8:], i[5], i[6]))

        playlist_shuffle = input("\n\n||| Shuffle playlist? (Y/N): ").strip().lower() == "y"
        playlist_loop = input("||| Loop playlist? (Y/N): ").strip().lower() == "y"

        while True:
            if playlist_shuffle:
                random.shuffle(loaded_results)
            for i in range(0, len(loaded_results)):
                play_song(loaded_results[i])
            if not playlist_loop:
                break
    except:
        pass

def main():
    selected_mode = input("\n||| Enter 'S' (search mode), 'R' (random song), 'L' (random list), or 'P' (playlist)\n||| Add 'V' to the end to play video instead of audio: ").lower().strip()
    global play_video
    play_video = len(selected_mode) > 1 and selected_mode[1] == "v"

    while True:
        match selected_mode[0]:
            case "s":
                begin_search_mode()
            case "r":
                begin_random_mode()
            case "l":
                begin_list_mode()
            case "p":
                begin_playlist_mode()
            case _:
                break

# Driver code
song_list = main_init()
play_video = False
while True:
    main()