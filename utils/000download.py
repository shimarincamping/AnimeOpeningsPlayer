import os
import subprocess

command_template = "yt-dlp -c -o \"%(title)s.%(ext)s\" "

def try_downloading(file, timeout=15, retries=100):
    attempt = 1
    command = command_template + file

    while attempt < retries:
        try:
            print("\n\n[~] Downloading file: " + file)
            p = subprocess.Popen(command, start_new_session=True, shell=True, text=True)
            p.wait(timeout=timeout)
            return True
        except:
            attempt += 1
            print("\n\n[!] Too slow! Restarting download for file: " + file + " (Attempt: " + str(attempt) + ")")
            os.system("taskkill /PID {} /T /F".format(p.pid))
    return False


with open("000batch.txt") as download_list:
    queue = [x for x in download_list.read().split("\n") if x.split("/")[-1] not in os.listdir(".")]

failed_files = [i for i in queue if not try_downloading(i)]
print("The following files failed to download:\n" + "\n".join(failed_files))