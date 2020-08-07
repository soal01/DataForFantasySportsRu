import requests
import time
import os.path

URL_H2H = "https://fantasy-h2h.ru/analytics/fantasy_players_statistics"
URL_SPORTS_RU = "https://sports.ru/"


class Players_stats_and_names_loader:
    def __init__(self, season):
        self.id_of_season = season["id_of_season"]
        self.dir_of_season = season["dir_of_season"]
        self.h2h_id_of_season = season["h2h_id_of_season"]

    def load_file(self, url, path):
        req = requests.get(url)
        if req.status_code == 200:
            with open(path, "w") as f:
                f.write(req.content.decode())
            print(path, "successfully downloaded")
        time.sleep(1)

    def load_names(self):
        self.load_file(f"{URL_H2H}/{self.h2h_id_of_season}", f"{self.dir_of_season}/players.html")
        for i in range(1, 6):
            self.load_file(f"{URL_H2H}/{self.h2h_id_of_season}?offset={i}00", f"{self.dir_of_season}/players{i}.html")

    def load_stats(self, player_links):
        for link in player_links:
            new_link = link
            if new_link.find("tags") != -1:
                new_link = link.split("/")[1]
            if not os.path.exists(f"{self.dir_of_season}/{new_link}.html"):
                self.load_file(f"{URL_SPORTS_RU}{link}/stat/?s={self.id_of_season}&t=31",
                               f"{self.dir_of_season}/{new_link}.html")


