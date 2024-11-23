
class Clock:
    def __init__(self):
        self.day = 1
        self.year = 1
        self.month = 0

        self.hour = 0

    def tick(self):
        self.hour += 1
        if self.hour > 23:
            self.hour -= 24
            self.day += 1
            if self.day > 30:
                self.month += 1
                self.day = 1
                if self.month > 12:
                    self.month = 1
                    self.year += 1


    def __repr__(self):
        s = f"{str(self.year).zfill(4)}-{str(self.month).zfill(2)}-{str(self.day).zfill(2)} "
        s += f"{str(self.hour).zfill(2)}:00"
        return s
