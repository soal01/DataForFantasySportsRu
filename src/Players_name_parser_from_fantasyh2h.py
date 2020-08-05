
class Players_name_parser_from_fantasyh2h:
    def __init__(self, filename):
        with open(filename, "r") as f:
            self.string = f.read()

    def set_file(self, filename):
        with open(filename, "r") as f:
            self.string = f.read()

    def cut(self, substr):
        self.string = self.string[self.string.find(substr):]

    def cut_n_symbols(self, n):
        self.string = self.string[n:]

    def parse_simple_data(self):
        pos = self.string.find(" <")
        data = self.string[:pos]
        self.string = self.string[pos:]
        return data

    def parse_players_link(self):
        pos = self.string.find("/\"")
        link = self.string[:pos]
        self.string = self.string[pos:]
        return link

    def parse_player(self):
        data = []
        self.cut("<td")
        self.cut_n_symbols(1)
        self.cut("<td")
        self.cut(">")
        self.cut_n_symbols(2)
        data.append(self.parse_simple_data())

        self.cut("<td")
        self.cut_n_symbols(1)
        self.cut("<td")
        self.cut(">")
        self.cut_n_symbols(2)
        data.append(self.parse_simple_data())

        self.cut("<td")
        self.cut(">")
        self.cut_n_symbols(2)
        data.append(self.parse_simple_data())

        self.cut("\"nowrap\"")
        self.cut("<a ")
        self.cut_n_symbols(1)
        self.cut("<a ")
        self.cut("https://sports.ru/")
        self.cut_n_symbols(len("https://sports.ru/"))
        link = self.parse_players_link()

        self.cut("</tr")
        # print(data, link)
        data.append(link)
        return data

    def parse(self):
        data = []
        self.cut("<table")
        self.cut("<tbody")
        pos = self.string.find("<tr")
        while pos != -1:
            ans = self.parse_player()
            data.append(ans)
            pos = self.string.find("<tr")
        return data

    def get_all_names(self, season):
        ans = []
        self.set_file(f"{season['dir_of_season']}/players.html")
        ans.extend(self.parse())
        for i in range(1, 6):
            self.set_file(f"{season['dir_of_season']}/players{i}.html")
            ans.extend(self.parse())
        return ans
