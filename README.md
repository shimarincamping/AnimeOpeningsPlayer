# Anime Openings Player

A simple program to search, filter, and stream anime openings


Opening Player:
- Windows-compatible
- Requires `mpv` to be executable on the command prompt
- Requires `gdown` to fetch updated data


Updater:
- Requires a copy of `000data.txt` downloaded by `.player.py`
- Requires a copy of column AA from [sheet](https://docs.google.com/spreadsheets/d/1_601RwB9Sl3yTJQ3k0IMI8o319iZXAV4/edit?usp=drive_link&ouid=108270624448384351060&rtpof=true&sd=true) in `000updatehistory.txt`
- New difficulty column is output in `000output.txt`
- Permanent renames to be excluded from discrepancy checks in `000exceptions.txt`


Utils:
- `000renamer.py` - renames all mp3 files to the anime title (requires `000data.txt`)
- `000renamer_webm.py` - renames all webm files to the anime title (requires `000data.txt`)
- `.xmltolist.py` - parses xml file downloaded from [scraper](https://malscraper.azurewebsites.net/) located in the `xmlfiles` subdirectory as a json string for `openingplayer/000playlists.json` (requires `000data.txt`)
- `.xmlgenerator.py`- generates xml file from newline-separated string to be batch added/moved via MAL/AniList import; can be filtered then copied from column T of [sheet](https://docs.google.com/spreadsheets/d/1_601RwB9Sl3yTJQ3k0IMI8o319iZXAV4/edit?usp=drive_link&ouid=108270624448384351060&rtpof=true&sd=true)
- `JSON to Excel.py` - converts old Song List UI JSON exports (not native AMQ export) to sheet-compatible TSV from `/convert` into `000output.txt`
- `000download.py` - downloads newline-separated video links in `000batch.txt` (kills processes and restarts download if the process takes too long)


Misc:
- `.amq.py` - song guessing game, requires all mp3s to be downloaded (stream option not yet available); enter string to guess, '/hint' for hangman-style hint, or '/pass' to skip (requires `000data.txt`)