from datetime import datetime
from pytube.cli import on_progress
from pytube import YouTube, streams

class Conversor():
    def __init__(self):
        self._urls = []
        self._number = int
        self._pathsafe = str
        self._datetime = datetime.now().strftime("%Y%m%d")
        self._config = r"/home/henrique/myfiles/projetos/pymusic/config.txt"

    
    def load_config(self):
        with open(self._config, "r") as file:
            for line in file.readlines():
                if "number=" in line:
                    self._number = int(line.split("=")[1].strip())
                elif "pathsafe=" in line:
                    self._pathsafe = line.split("=")[1].strip()
                elif "date=" in line:
                    if int(self._datetime) > int(line.split("=")[1]):
                        self._number = 0

    def write_config(self):
        with open(self._config, "w") as file:
            file.write(f"number={self._number}\n")
            file.write(f"pathsafe={self._pathsafe}\n")
            file.write(f"date={self._datetime}\n")


    def load_urls(self, path):
        with open(path, "r") as file:
            for line in file.readlines():
                self._urls.append(line)


    def conversor(self):
        for url in self._urls:
            try:
                self._number += 1
                yt = YouTube(url,
                             on_progress_callback = on_progress)

                aud = yt.streams.get_highest_resolution()
                aud = yt.streams.get_audio_only()
                name = f"AUD-{self._datetime}WA000000"
                name = name[:-len(str(self._number))]
                name = name + str(self._number) + ".mp3"
                aud.donwload(filename=name, output_path=self._pathsafe)
            except Exception as e:
                self._number -= 1
                continue

if __name__ == "__main__":
    con = Conversor()
    con.load_config()
    con.load_urls("/home/henrique/myfiles/projetos/pymusic/linkx.txt")
    print(con._urls)
    con.conversor()
    con.write_config()
