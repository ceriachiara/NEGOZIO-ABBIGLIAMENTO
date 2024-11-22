class Date:
    def __init__(self, day =1 , month =1, year =1900):
        self.date = [day, month, year]

    def is_valid(self):
        return self.verifica_data(self.date[0], self.date[1], self.date[2])

    def get_day(self):
        return self.date[0]

    def set_day(self, day):
        self.date[0] = day

    def get_month(self):
        return self.date[1]

    def set_month(self, month):
        self.date[1] = month

    def get_year(self):
        return self.date[2]

    def set_year(self, year):
        self.date[2] = year

    def verifica_data(self, day, month, year):
        if day < 1 or day > 31:
            return False
        if month < 1 or month > 12:
            return False
        if year < 1900 or year > 2900:
            return False
        if month in [4, 6, 9, 11] and day == 31:
            return False
        if month == 2:
            if day > 29:
                return False
            if day == 29 and not self.bisestile(year):
                return False
        return True

    def bisestile(self, year):
        if (year % 400 == 0) or ((year % 100 != 0) and (year % 4 == 0)):
            return True
        return False