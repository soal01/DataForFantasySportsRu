import csv

old_columns = ["position", "name", "cost", "date", "home team", "home goals", "away goals", "away team",
                "team", "start minute", "finish minute", "minutes", "goals", "penalties", "assists",
                "goals+assists", "yellow cards", "red cards", "clean sheets", "points"]
columns = []


class Players_stat_recorder:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=old_columns)
            writer.writeheader()

    def write_row(self, row):
        with open(self.filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def update_row(self, rows):
        for row in rows:
            self.calculate_clean_sheet(row)
            self.calculate_points(row)

    def calculate_clean_sheet(self, row):
        if row[4] == row[8]:
            row.append(int(row[6] == "0"))
        else:
            row.append(int(row[5] == "0"))

    def calculate_points(self, row):
        points = 0
        if int(row[11]) >= 60:
            points += 2
        else:
            points += 1
        points += int(row[-2]) * (-3)
        points += int(row[-3]) * (-1)
        points += int(row[14]) * 3
        if row[0] == "Вр" or row[0] == "Зщ":
            points += (int(row[12])) * 6
            points += int(row[-1]) * 4
            if row[4] == row[8]:
                points -= int(row[6]) // 2
            else:
                points -= int(row[5]) // 2
        elif row[0] == "Пз":
            points += (int(row[12])) * 5
            points += int(row[-1]) * 1
        elif row[0] == "Нп":
            points += (int(row[12])) * 4
        row.append(points)

    def write_rows(self, rows):
        for row in rows:
            self.write_row(row)


