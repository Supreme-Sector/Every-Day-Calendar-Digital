from datetime import date
import pickle

# List of tuples in the format (MM, DD)
# For example, if you missed March 14, you should include (3, 14) as an element of missed_dates
missed_dates = []

current_date = str(date.today())
current_year = int(current_date.split("-")[0])
current_month = int(current_date.split("-")[1])
current_day = int(current_date.split("-")[2])

def determine_feb_len(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return 29
            else:
                return 28
        else:
            return 29
    else:
        return 28

month_lengths = [31, determine_feb_len(current_year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

illumination_values = [[0 for i in range(month_lengths[j])] for j in range(12)]

for i in range(current_month-1):
    illumination_values[i] = [1 for j in range(month_lengths[i])]

for i in range(current_day-1):
    illumination_values[current_month-1][i] = 1

for date in missed_dates:
    month_index = date[0]-1
    day_index = date[1]-1
    illumination_values[month_index][day_index] = 0

filename = str(current_year)+"_calendar_data.pickle"
file = open(filename, "wb")
pickle.dump(illumination_values, file)
file.close()
