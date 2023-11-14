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
    
    # def aggregate(self, function, aggregation_key):
    #     temps = []
    #     for item1 in self.table:
    #         temps.append(float(item1[aggregation_key]))
    #     return function(temps)

    def __is_float(self, element):
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
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

    def pivot_table(self, keys_to_pivot_list, keys_to_aggregate_list, aggregate_func_list):

        # First create a list of unique values for each key
        unique_values_list = []

        # Here is an example of  unique_values_list for
        # keys_to_pivot_list = ['embarked', 'gender', 'class']
        # unique_values_list = [['Southampton', 'Cherbourg', 'Queenstown'], ['M', 'F'], ['3', '2','1']]
        pivot = []
        for keys in keys_to_pivot_list:
            table_selected = self.select(keys)
            # print(table_selected)
            temp = []
            for x in table_selected:
                for key, value in x.items():
                    if value not in temp:
                        temp.append(value)
            pivot.append(temp)

        # print('pivot',pivot)



        # temps =[]
        #
        # for keys in keys_to_pivot_list:
        #     # print(self.select(keys))
        #     selected_keys = self.select([keys])
        #     # print(self.select([keys]))
        #     for i in selected_keys:
        #         if i.values() not in temps:
        #     #         temps.append(i.values())
        #     # print(temps)
        # # print(self.select(keys_to_pivot_list))


        # Get the combination of unique_values_list
        # You will make use of the function you implemented in Task 2

        import combination_gen

        # code that makes a call to combination_gen.gen_comb_list
        # print(combination_gen.gen_comb_list(unique_values_list))
        # Example output:
        # [['Southampton', 'M', '3'],
        #  ['Cherbourg', 'M', '3'],
        #  ...
        #  ['Queenstown', 'F', '1']]

        # code that filters each combination

        # for each filter table applies the relevant aggregate functions
        # to keys to aggregate
        # the aggregate functions is listed in aggregate_func_list
        # to keys to aggregate is listed in keys_to_aggregate_list
        # return a pivot table
        # print('here',self.table)
        # print(self.table[0])
        # for i in self.table[0]:
        #     if i == 'fare':
        #         print(self.table[0][i])

        # select keys for aggregation
        # temps_for_aggregation = []
        # for key in keys_to_aggregate_list:
        #     # selected_info = []
        #     selected = self.select([key])
        #     # selected_info.append(selected)
        #     temps_for_aggregation.append(selected)
        # print(temps_for_aggregation)

        # making pivot combinations
        unique_pivot = []
        comb_pivot = combination_gen.gen_comb_list(pivot)
        # print(comb_pivot)
        for i in comb_pivot:
            rn = copy.copy(self)
            aggregated = []
            # print(comb_pivot)
            # aggregation
            for index in range(len(keys_to_pivot_list)):
                rn = rn.filter(lambda x: x[keys_to_pivot_list[index]] == i[index])
                # print(rn)

            for index in range(len(keys_to_aggregate_list)):
                val = rn.aggregate(aggregate_func_list[index], keys_to_aggregate_list[index])
                # print(val)
                aggregated.append(val)

            unique_pivot.append([i,aggregated])
        return unique_pivot

            # print(j)
            # for k in j:
            #     print(j)
            #         print(i,k)
            #         rn = rn.filter(lambda x: x[i] == k)
            #         print(rn)




        # for u in comb_pivot:
        #     aggregate_value = []
        #     now = copy.copy(self)
        #     for kpv in range(len(u)):
        #         now = now.filter(lambda x: x[keys_to_pivot_list[kpv]] == u[kpv])
        #         print(now)
        #     for vpv in range(len(keys_to_aggregate_list)):
        #         value = now.aggregate(aggregate_func_list[vpv], keys_to_aggregate_list[vpv])
        #         aggregate_value.append(value)
        #         list_list.append([u, aggregate_value])
        # return list_list






        # aggregation
        #     aggregated = []
        #     for i in keys_to_pivot_list:
        #         for j in unique_pivot:
        #             for k in j:
        #                 # print(k)
        #                 # print(i,k)
        #                 rn = rn.filter(lambda x: x[i] == k)
        #                 print(rn)

        # for i in range(len(keys_to_pivot_list)):
        #     for j in range(len(unique_pivot)):
        #         for k in range(len(unique_pivot[j])):
        #             # print(i,unique_pivot[j][k])
        #             filtered = rn.filter(lambda x: x[keys_to_pivot_list[i]] == unique_pivot[j][k])

        # combine = combination_gen.gen_comb_list(unique_values_list)
        # list_list = []
        # for u in combine:
        #     aggregate_value = []
        #     now = copy.copy(self)
        #     for kpv in range(len(u)):
        #         now = now.filter(lambda x: x[keys_to_pivot_list[kpv]] == u[kpv])
        #     for vpv in range(len(keys_to_aggregate_list)):
        #         value = now.aggregate(aggregate_func_list[vpv], keys_to_aggregate_list[vpv])
        #         aggregate_value.append(value)
        #         list_list.append([u, aggregate_value])
        # return list_list

        # my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'yes').filter(lambda x: x['coastline'] == 'no')
        # print("Min temp:", my_table3_filtered.aggregate(lambda x: min(x), 'temperature'))

        # print(unique_pivot)



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
# print(my_table3.table_name,my_table3.table)



# table4 = Table('titanic', titanic)
# my_DB.insert(table4)
my_table5 = my_DB.search('titanic')
my_pivot = my_table5.pivot_table(['embarked', 'gender', 'class'], ['fare', 'fare', 'fare', 'last'], [lambda x: min(x), lambda x: max(x), lambda x: sum(x)/len(x), lambda x: len(x)])
print(my_pivot)

# pivot test case 1
my_pivot_1 = my_table3.pivot_table(['position'], ['passes', 'shots'], [lambda x: sum(x)/len(x), lambda x: len(x)])
print(my_pivot_1)

# pivot test case 2
countries_ext = my_table1.join(table2, 'country')
my_pivot_2 = countries_ext.pivot_table(['EU','coastline'], ['temperature','latitude', 'latitude'], [lambda x: sum(x)/len(x),lambda x: min(x), lambda x: max(x)])
print(my_pivot_2)


# pivot test case 3
my_pivot_3 = my_table5.pivot_table(['class', 'gender', 'survived'], ['survived', 'fare'], [lambda x: len(x),lambda x: sum(x)/len(x)])
print(my_pivot_3)
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
