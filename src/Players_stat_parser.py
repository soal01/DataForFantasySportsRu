import os.path


class Players_stat_parser:
    def __init__(self, filename):
        with open(filename, "r") as f:
            self.string = f.read()

    def cut(self, substr):
        self.string = self.string[self.string.find(substr):]

    def cut_n_symbols(self, n):
        self.string = self.string[n:]

    def parse_date(self):
        pos = self.string.find("\n<")
        date = self.string[:pos]
        self.string = self.string[pos:]
        return date

    def parse_team(self):
        pos = self.string.find("<")
        is_his_team = False
        if pos == 0:
            self.cut_n_symbols(3)
            pos = self.string.find("<")
            is_his_team = True
        opponent = self.string[:pos]
        self.string = self.string[pos:]
        return opponent, is_his_team

    def parse_score(self):
        pos = self.string.find(" :")
        home = self.string[:pos]
        self.string = self.string[pos:]
        self.cut_n_symbols(3)
        pos = self.string.find("<")
        away = self.string[:pos]
        self.string = self.string[pos:]
        return [home, away]

    def parse_simple_data(self):
        self.cut("<td")
        # self.cut_n_symbols(4)
        self.cut(">")
        self.cut_n_symbols(1)
        pos = self.string.find("<")
        if pos == 0:
            return '0'
        else:
            data = self.string[:pos]
            self.string = self.string[pos:]
            return data

    def parse_league(self):
        pos = self.string.find("<")
        ans = self.string[:pos]
        self.string = self.string[pos:]
        return ans

    def parse_match(self):
        data = []
        self.cut("\"name-td alLeft bordR\">")
        self.cut_n_symbols(23)
        self.cut(">")
        self.cut_n_symbols(2)
        data.append(self.parse_date())

        self.cut("<a")
        self.cut(">")
        self.cut_n_symbols(1)
        league = self.parse_league()
        if league != 'Россия. Премьер-лига':
            return None
        is_his_team_home = False
        self.cut("\"owner-td\"")
        self.cut("href")
        self.cut(">")
        self.cut_n_symbols(1)
        ans, is_his_team_home = self.parse_team()
        data.append(ans)

        self.cut("\"score-td\"")
        self.cut("<b>")
        self.cut_n_symbols(3)
        data.extend(self.parse_score())

        self.cut("\"guests-td bordR\"")
        self.cut("href")
        self.cut(">")
        self.cut_n_symbols(1)
        data.append(self.parse_team()[0])

        # data.append(is_his_team_home)
        if is_his_team_home:
            data.append(data[-4])
        else:
            data.append(data[-1])

        for i in range(9):
            ans = self.parse_simple_data()
            if ans != 'Неиспользованная замена':
                data.append(ans)
            else:
                return None

        # print(data)
        return data

    def set_input_file(self, filename):
        with open(filename, "r") as f:
            self.string = f.read()

    def parse_player(self, filename=None):
        if filename:
            self.set_input_file(filename)
        data = []
        self.cut("<table")
        pos = self.string.find("<tr>")
        while pos != -1:
            ans = self.parse_match()
            if ans:
                if ans[0] != '':
                    data.append(ans)
            pos = self.string.find("<tr>")

        '''for el in data:
            print(el)'''
        return data

    def get_rows(self, names_dir, names):
        rows = []
        for name in names:
            link = name.pop()
            if link.find("tags") != -1:
                link = link.split("/")[1]
            if os.path.exists(f"{names_dir}/{link}.html"):
                data = self.parse_player(f"{names_dir}/{link}.html")
                for el in data:
                    new_row = name + el
                    rows.append(new_row)
        return rows
