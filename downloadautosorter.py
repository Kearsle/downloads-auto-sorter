import os
import time
import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

downloads_dir = os.path.expanduser("~/Downloads")
image_dir = os.path.expanduser("~/Pictures/Downloaded Pictures")
installers_dir = os.path.expanduser("~/Documents/Installers")
video_dir = os.path.expanduser("~/Movies/Downloaded Videos")
document_dir = os.path.expanduser("~/Documents/Downloaded Files")

class colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def makeUnique(dest, name):
    nameSplit = name.rsplit('.', 1)
    i = 1
    while os.path.exists(dest + "/" + nameSplit[0] + " ({}).".format(i) + nameSplit[1]):
        i += 1
    return nameSplit[0] + " ({}).".format(i) + nameSplit[1]

def move(dest, entry, name):
    file_exists = os.path.exists(dest + "/" + name)
    if file_exists: 
        name = makeUnique(dest, name)
    print(colors.CYAN + " - " + colors.GREEN + name + colors.END + " has been moved to " + colors.RED + dest + colors.END + ".")
    shutil.move(entry, "{}/{}".format(dest, name))

class FileMoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        num = 0
        with os.scandir(downloads_dir) as entries:
            for entry in entries:
                name = entry.name
                if name.endswith('.png') or name.endswith('.jpg') or name.endswith('.jpeg'):
                    move(image_dir, entry, name)
                elif name.endswith('.mov') or name.endswith('.mp4'):
                    move(video_dir, entry, name)
                elif name.endswith('.dmg'):
                    move(installers_dir, entry, name)
                elif name.endswith('.pdf') or name.endswith('.docx'):
                    move(document_dir, entry, name)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = downloads_dir
    event_handler = FileMoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    os.system('clear')
    print(colors.BOLD + colors.UNDERLINE + "Downloads Auto Sorter Started!" + colors.END)
    FileMoveHandler().on_modified("")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()