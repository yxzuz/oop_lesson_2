import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))  # list of dict was obtained

countries = []
with open(os.path.join(__location__, 'Countries.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        countries.append(dict(r))

players = []
with open(os.path.join(__location__, 'Players.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        players.append(dict(r))

teams = []
with open(os.path.join(__location__, 'Teams.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        teams.append(dict(r))

titanic = []
with open(os.path.join(__location__, 'Titanic.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        titanic.append(dict(r))
# NOTE we can use 'team' key to join tables


class DB:
    def __init__(self):
        self.database = []  # tables will be inserted here

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


import copy


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table
    
    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table
    
    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table
    
    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            temps.append(float(item1[aggregation_key]))
        return function(temps)
    
    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def __str__(self):
        return self.table_name + ':' + str(self.table)


#  create tables from data sets
table1 = Table('cities', cities)
table2 = Table('countries', countries)
table3 = Table('players', players)  # NOTE players is list of dict
table4 = Table('teams', teams)
table5 = Table('titanic', titanic)

my_DB = DB()  # create database to store all tables
my_DB.insert(table1)
my_DB.insert(table2)
my_DB.insert(table3)
my_DB.insert(table4)
my_DB.insert(table5)
my_table1 = my_DB.search('cities')
my_table3 = my_DB.search('players')
print(my_table3.table_name,my_table3.table)


# player on a team with “ia” in the team name played less than 200 minutes and made more than 100 passes?
# for index in range(len(players)):
#     # for items in range(len(players[index])):
#     int(players[index]['passes'])
#     int(players[index]['minutes'])
    # for key in range(len(index[table3])):
    #     int(table3[key]['passes'])


# player on a team with “ia” in the team name played less than 200 minutes and made more than 100 passes?
filtered_table3 = table3.filter(lambda x: int(x['passes']) > 100).filter(lambda x: int(x['minutes']) < 200).filter(lambda x: 'ia' in x['team'])
print(type(filtered_table3))

# Select to display the player surname, team, and position

# print("Test select: only displaying two fields, surname, team, and position
my_filtered_table3_selected = filtered_table3.select(['surname', 'team', 'position'])
print(my_filtered_table3_selected)
print()


# The average number of games played for teams ranking below 10 versus teams ranking above or equal 10
rank_below_ten = table4.filter(lambda x: int(x['ranking']) < 10)
# print(rank_below_ten)
avg1 = rank_below_ten.aggregate(lambda x: sum(x)/len(x), 'ranking')
print('Avg ranking < 10: ', avg1)

rank_ten_or_more = table4.filter(lambda x:int(x['ranking']) >= 10)
avg2 = rank_ten_or_more.aggregate(lambda x: sum(x)/len(x), 'ranking')
print('Avg ranking >= 10: ', avg2)

# The average number of passes made by forwards versus by midfielders

# join table

players_ext = table3.join(table4, 'team')
print(players_ext)
# avg_by_forwards
print('forward avg:', players_ext.filter(lambda x:x['position'] == 'forward').aggregate(lambda x: sum(x)/len(x), 'passes'))


# avg_by_mid
print('mid avg:', players_ext.filter(lambda x: x['position'] == 'midfielder').aggregate(lambda x: sum(x)/len(x), 'passes'))

# The average fare paid by passengers in the first class versus in the third class
# first class avg
print('First class avg', table5.filter(lambda x: x['class'] == "1").aggregate(lambda x: sum(x)/len(x), 'fare'))

# third class avg
print('Third class avg', table5.filter(lambda x: x['class'] == "3").aggregate(lambda x: sum(x)/len(x), 'fare'))


# The survival rate of male versus female passengers
#male rates
total_male = table5.filter(lambda x: x['gender'] == "M")
total_female = table5.filter(lambda x: x['gender'] == "F")
male_survival = total_male.filter(lambda x: x['survived'] == "yes")
female_survival = total_female.filter(lambda x: x['survived'] == "yes")
print('Male survival rate: ',len(male_survival.table)/len(total_male.table))
print('Female survival rate: ',len(female_survival.table)/len(total_female.table))
#WHY DOT TABLE???

# Find the total number of male passengers embarked at Southampton
male_southampton = total_male.filter(lambda x: x['embarked'] == "Southampton")
print('male passengers embarked at Southampton:',len(male_southampton.table))


# print("Test filter: only filtering out cities in Italy")
# my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
# print(my_table1_filtered)
# print()
#
# print("Test select: only displaying two fields, city and latitude, for cities in Italy")
# my_table1_selected = my_table1_filtered.select(['city', 'latitude'])
# print(my_table1_selected)
# print()
#
# print("Calculting the average temperature without using aggregate for cities in Italy")
# temps = []
# for item in my_table1_filtered.table:
#     temps.append(float(item['temperature']))
# print(sum(temps)/len(temps))
# print()
#
# print("Calculting the average temperature using aggregate for cities in Italy")
# print(my_table1_filtered.aggregate(lambda x: sum(x)/len(x), 'temperature'))
# print()
#
# print("Test join: finding cities in non-EU countries whose temperatures are below 5.0")
# my_table2 = my_DB.search('countries')
# my_table3 = my_table1.join(my_table2, 'country')
# my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(lambda x: float(x['temperature']) < 5.0)
# print(my_table3_filtered.table)
# print()
# print("Selecting just three fields, city, country, and temperature")
# print(my_table3_filtered.select(['city', 'country', 'temperature']))
# print()
#
# print("Print the min and max temperatures for cities in EU that do not have coastlines")
# my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'yes').filter(lambda x: x['coastline'] == 'no')
# print("Min temp:", my_table3_filtered.aggregate(lambda x: min(x), 'temperature'))
# print("Max temp:", my_table3_filtered.aggregate(lambda x: max(x), 'temperature'))
# print()
#
# print("Print the min and max latitude for cities in every country")
# for item in my_table2.table:
#     my_table1_filtered = my_table1.filter(lambda x: x['country'] == item['country'])
#     if len(my_table1_filtered.table) >= 1:
#         print(item['country'], my_table1_filtered.aggregate(lambda x: min(x), 'latitude'), my_table1_filtered.aggregate(lambda x: max(x), 'latitude'))
# print()
