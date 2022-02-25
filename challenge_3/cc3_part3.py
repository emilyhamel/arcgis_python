## CODING CHALLENGE 3
# Part 3: working with CSV

import csv

# create lists to contain date and co2 values
year_list = []
month_list = []
value = []

with open("co2-ppm-daily.csv") as co2_daily:
    csv_reader = csv.reader(co2_daily, delimiter=',')
    next(co2_daily)
    for row in csv_reader:
        year, month, day = row[0].split("-")
        if year not in year_list:
            year_list.append(year)  # splitting and populating the year list in this step to prepare yearly average
            if month not in month_list:
                month_list.append(month)
        value.append(float(row[1]))  # adding co2 values into the empty value list

# Minimum, maximum and average for the entire dataset.
print("Minimum Value: " + str(min(value)))
print("Maximum Value: " + str(max(value)))
print("Average: " + str((sum(value)/len(value))) + "\n")


# Annual average for each year in the dataset.
year_dictionary = {}
for year in year_list:
    temp_year_list = []
    with open("co2-ppm-daily.csv") as co2_daily:
        csv_reader = csv.reader(co2_daily, delimiter=',')
        next(co2_daily)
        for row in csv_reader:
            year_split, month_split, day_split = row[0].split("-")
            # if "_split" isn't added it only looks at the last year in the dataset
            if year_split == year:
                temp_year_list.append(float(row[1]))  # add co2 value to the temp_year_list
    year_dictionary[year] = str(sum(temp_year_list) / len(temp_year_list))  # populate with average for each year

print("Yearly Average: ")
print(year_dictionary)


# Seasonal Averages
# create empty lists for each season
spring = []  # March 03, April 04, May 05
summer = []  # June 06, July 07, August 08
fall = []  # September 09, October 10, November 11
winter = []  # December 12, January 01, February 02
with open("co2-ppm-daily.csv") as co2_daily:
    csv_reader = csv.reader(co2_daily, delimiter=',')
    next(co2_daily)
    for row in csv_reader:
        year, month, day = row[0].split("-")  # split the date column to add month values into corresponding season list
        if month == "03":
            spring.append(float(row[1]))
        if month == "04":
            spring.append(float(row[1]))
        if month == "05":
            spring.append(float(row[1]))
        if month == "06":
            summer.append(float(row[1]))
        if month == "07":
            summer.append(float(row[1]))
        if month == "08":
            summer.append(float(row[1]))
        if month == "09":
            fall.append(float(row[1]))
        if month == "10":
            fall.append(float(row[1]))
        if month == "11":
            fall.append(float(row[1]))
        if month == "12":
            winter.append(float(row[1]))
        if month == "01":
            winter.append(float(row[1]))
        if month == "02":
            winter.append(float(row[1]))

print("Seasonal Averages:")
print("Spring Average: " + str(sum(spring)/len(spring)))
print("Summer Average: " + str(sum(summer)/len(summer)))
print("Fall Average: " + str(sum(fall)/len(fall)))
print("Winter Average: " + str(sum(winter)/len(winter)) + "\n")


# Calculate the anomaly for each value in the dataset relative to the mean for the entire time series.
overall_average = sum(value)/len(value)
anomaly = {}
with open("co2-ppm-daily.csv") as co2_daily:
    csv_reader = csv.reader(co2_daily, delimiter=',')
    next(co2_daily)
    for row in csv_reader:
        year, month, day = row[0].split("-")
        anomaly[year] = float(row[1]) - overall_average
        # subtract the overall mean from the co2 values to find the anomaly based on yearly data
print("Anomaly per Year:")
print(anomaly)

# calculating per day returns an overwhelming amount of data
# but if finding the anomaly of each individual value is the goal:
# overall_average = sum(value)/len(value)
# anomaly = {}
# with open("co2-ppm-daily.csv") as co2_daily:
#     csv_reader = csv.reader(co2_daily, delimiter=',')
#     next(co2_daily)
#     for row in csv_reader:
#         anomaly[row[0]] = float(row[1]) - overall_average
# print("Anomaly per Day:")
# print(anomaly)



