from tkinter import *
from datetime import date
import pickle

current_date = str(date.today())

root = Tk()

root.title("The Every Day Calendar - Digital")
root.iconbitmap(r"calendar_icon.ico")

class Calendar(Canvas):
    def __init__(self, master, year):
        super().__init__(master, width=480, height=680, background="#c9863e")
        self.year = year
        self.months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        self.month_lengths = [31, self.__determine_feb_len(), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.illumination_values = self.__load_calendar_data()

        self.create_text(240, 20, font=("Impact", 20), text=str(year))
        for i in range(12):
            column = 20 + 40 * i
            self.create_text(column, 56, text=self.months[i], font=("Bahnschrift Condensed", 10))
            for j in range(self.month_lengths[i]):
                date_tag = str(self.year)+"-"+str(i+1).zfill(2)+"-"+str(j+1).zfill(2)
                self.__add_day(column, 72 + j * 20, date_tag, self.illumination_values[i][j])

        self.tag_bind(current_date, "<Button-1>", self.__illuminate)
        self.pack()
    def __update_calendar_data(self):
        filename = str(self.year)+"_calendar_data.pickle"
        file = open(filename, "wb")
        pickle.dump(self.illumination_values, file)
        file.close()

    def __load_calendar_data(self):
        filename = str(self.year) + "_calendar_data.pickle"
        try:
            file = open(filename, "rb")
        except:
            file = open(filename, "wb")
            new_illumination_values = [[0 for i in range(self.month_lengths[j])] for j in range(12)]
            pickle.dump(new_illumination_values, file)
            file.close()
            file = open(filename, "rb")
        data = pickle.load(file)
        file.close()
        return data


    def __determine_feb_len(self):
        if self.year % 4 == 0:
            if self.year % 100 == 0:
                if self.year % 400 == 0:
                    return 29
                else:
                    return 28
            else:
                return 29
        else:
            return 28

    def __add_day(self, x, y, day, illumination_value):
        if illumination_value == 1:
            colour = "#f5ed0a"
        else:
            colour = "black"
        points = [x - 7, y - 9, x + 7, y - 9, x + 11, y, x + 7, y + 9, x - 7, y + 9, x - 11, y]
        self.create_polygon(points, outline=colour, fill="#c9863e", tags=day)  # Change to #f5ed0a when illuminated
        self.create_text(x, y, text=int(day.split('-')[2]), font=("Bahnschrift Condensed", 9), fill=colour, tags=day)

    def __illuminate(self, event):
        polygon = event.widget.find_closest(event.x, event.y)
        tag = self.gettags(polygon)[0]
        items = self.find_withtag(tag)
        for item in items:
            if self.type(item) == "polygon":
                self.itemconfig(item, outline="#f5ed0a")
            else:
                self.itemconfig(item, fill="#f5ed0a")
        month_num = int(tag.split("-")[1])
        day_num = int(tag.split("-")[2])
        self.illumination_values[month_num-1][day_num-1] = 1
        self.__update_calendar_data()


current_year = int(current_date.split("-")[0])
calendar = Calendar(root, year=current_year)

root.mainloop()
