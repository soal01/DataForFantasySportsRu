import requests
import time
from src.Players_stat_parser import Players_stat_parser
from src.Players_name_parser_from_fantasyh2h import Players_name_parser_from_fantasyh2h
from src.Players_stats_and_names_loader import Players_stats_and_names_loader
from src.Players_stat_recorder import Players_stat_recorder
'''league_id = 31
player_link = "tags/140567221"
season_id = 6297
# #url = f"https://www.sports.ru/fantasy/football/player/info/{league_id}/{player_id}.html?s={season_id}"
url = f"https://sports.ru/{player_link}/stat/?s={season_id}&t={league_id}"
# https://www.sports.ru/tags/140567221/stat/?s=6297&t=31
req = requests.get(url)
if req.status_code == 200:
    with open(f"src/html_files/{player_link.split('/')[1]}_{season_id}.html", "w") as f:
        f.write(req.content.decode())
        print(player_link, "successfully downloaded")
'''

# url = 'https://fantasy-h2h.ru/analytics/fantasy_team_players/106'
'''for i in range(1, 6):
    url = f'https://fantasy-h2h.ru/analytics/fantasy_players_statistics/106?offset={i}00'
    req = requests.get(url)
    if req.status_code == 200:
        with open(f"src/html_files/2017_2018_rpl/players{i}.html", "w") as f:
            f.write(req.content.decode())
    time.sleep(1)
    print("OK!")
'''
# parser = Players_stat_parser("src/html_files/quincy-promes_6297.html")
# parser.parse_player()

seasons = {
    "2017-2018":
        {
            "id_of_season": 6297,
            "dir_of_season": "src/html_files/2017_2018_rpl",
            "h2h_id_of_season": 106,
        },
    "2018-2019":
        {
            "id_of_season": 6886,
            "dir_of_season": "src/html_files/2018_2019_rpl",
            "h2h_id_of_season": 130
        },
    "2019-2020":
        {
            "id_of_season": 7371,
            "dir_of_season": "src/html_files/2019_2020_rpl",
            "h2h_id_of_season": 155
        }
    }


'''parser = Players_name_parser_from_fantasyh2h("src/html_files/2017_2018_rpl/players.html")
parser.parse()
'''

'''loader = Players_stats_and_names_loader(seasons["2019-2020"])
loader.load_names()
'''

'''
parser = Players_name_parser_from_fantasyh2h("src/html_files/2019_2020_rpl/players.html")
names = parser.get_all_names(seasons['2019-2020'])
links = []
for name in names:
    links.append(name[-1])
loader = Players_stats_and_names_loader(seasons['2019-2020'])
loader.load_stats(links)
'''


parser = Players_name_parser_from_fantasyh2h("src/html_files/2017_2018_rpl/players.html")
names = parser.get_all_names(seasons['2017-2018'])
parser = Players_stat_parser("src/html_files/2017_2018_rpl/akinfeev.html")
rows = parser.get_rows(seasons['2017-2018']["dir_of_season"], names)
recorder = Players_stat_recorder("src/csv_files/2017-2018_rpl.csv")
for row in rows:
    print(row)
    recorder.calculate_clean_sheet(row)
    recorder.calculate_points(row)
recorder.write_rows(rows)

