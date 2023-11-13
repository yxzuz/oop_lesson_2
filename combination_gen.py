def gen_comb_list(list_set):
    """
        Parameters:
            list_set: a list of lists where each contains at least one element

        Returns:
            a list of lists, each of which is made from a combination of elements in each list in list_set

        Examples:
            gen_comb_list([[1, 2, 3]]) returns [[1], [2], [3]]
            gen_comb_list([[1, 2, 3], [4, 5]])
            returns [[1, 4], [2, 4], [3, 4],
                    [1, 5], [2, 5], [3, 5]]
            gen_comb_list([[1, 2, 3], [4, 5], [6, 7, 8]])
            returns [[1, 4, 6], [2, 4, 6], [3, 4, 6],
                    [1, 5, 6], [2, 5, 6], [3, 5, 6],
                    [1, 4, 7], [2, 4, 7], [3, 4, 7],
                    [1, 5, 7], [2, 5, 7], [3, 5, 7],
                    [1, 4, 8], [2, 4, 8], [3, 4, 8],
                    [1, 5, 8], [2, 5, 8], [3, 5, 8]]
    """

    import copy

    def gen_comb_list_recursive(list_set):
        if len(list_set) == 1:
            start_list = []
            for item in list_set[0]:
                start_list.append([item])
            return start_list
        comb_list_temp = gen_comb_list_recursive(list_set[0:-1])
        start_list = []
        for list_item in comb_list_temp:
            for val in list_set[-1]:
                temp_item = copy.deepcopy(list_item)
                temp_item.append(val)
                start_list.append(temp_item)
        return start_list

    comb_list = gen_comb_list_recursive(list_set)
    return comb_list
    # print("Test gen_comb_list")
    # x = [1, 2, 3]
    # y = [4, 5]
    # z = [6, 7, 8]
    # u = [9, 10]
    # comb_list = gen_comb_list_recursive([x])  # [[1, 2, 3]]
    # print(comb_list)
    # comb_list = gen_comb_list_recursive([x, y])  # [[1, 2, 3],[4, 5]]
    # print(comb_list)
    # comb_list = gen_comb_list_recursive([x, y, z]) # [[1, 2, 3],[4, 5], [6, 7, 8]]
    # print(comb_list, len(comb_list), [x, y, z])

# Test
# gen_comb_list([[], []])

# gen_comb_list([[1, 2, 3]])
# returns [[1], [2], [3]]
# print()

# print(gen_comb_list([[1, 2, 3], [4, 5]]))
    # returns [[1, 4], [2, 4], [3, 4],
    #         [1, 5], [2, 5], [3, 5]]



# gen_comb_list([[1, 2, 3], [4, 5], [6, 7, 8]])
# returns[[1, 4, 6], [2, 4, 6], [3, 4, 6],
# [1, 5, 6], [2, 5, 6], [3, 5, 6],
# [1, 4, 7], [2, 4, 7], [3, 4, 7],
# [1, 5, 7], [2, 5, 7], [3, 5, 7],
# [1, 4, 8], [2, 4, 8], [3, 4, 8],
# [1, 5, 8], [2, 5, 8], [3, 5, 8]]



# my = [[1, 2, 3], [4, 5]]
# second = [[1, 2, 3], [4, 5], [6, 7, 8]]
# print(my[0])
# print(my[1])
# print([my[0][0],my[1][0]])
# print([[my[0][0],my[1][0]], [my[0][1],my[1][1]]])
# print([[second[0][0],second[1][0],second[2][0]]])


#with help
# def gen_comb_list(list_set):
#     if not list_set:
#         return []
#
#     def cartesian_product(index, current_combination):
#         if index == len(list_set):
#             return [current_combination]
#
#         current_list = list_set[index]
#         combinations = []
#         for element in current_list:
#             new_combination = current_combination + [element]
#             combinations.extend(cartesian_product(index + 1, new_combination))
#         return combinations
#
#     return cartesian_product(0, [])
#
# # Examples:
# print(gen_comb_list([[1, 2, 3]))  # Output: [[1], [2], [3]]
# print(gen_comb_list([[1, 2, 3], [4, 5]])  # Output: [[1, 4], [2, 4], [3, 4], [1, 5], [2, 5], [3, 5]]
# print(gen_comb_list([[1, 2, 3], [4, 5], [6, 7, 8]])  # Output: [[1, 4, 6], [2, 4, 6], [3, 4, 6], [1, 5, 6], [2, 5, 6], [3, 5, 6], [1, 4, 7], [2, 4, 7], [3, 4, 7], [1, 5, 7], [2, 5, 7], [3, 5, 7], [1, 4, 8], [2, 4, 8], [3, 4, 8], [1, 5, 8], [2, 5, 8], [3, 5, 8]]

# failed
# if len(list_set) == 1:
#     for i in list_set:
#         my_list = []
#         for j in i:
#             my_list.append([j])
#     print(my_list)
#     #return my_list

# for i in range(len(list_set[1:len(list_set)])):
#     temp.append([x, y[0]])
#     while True:
#         i += 1
#         if i >= len(y):
#             break
#         temp.append([x,y[i]])

# return temp

#     my_sublist.append(list_set[i][j])
# temp.append(my_sublist)


# working on
# i += 1

# for y in list_set[1:]:
#     a = 0
#     # print(([x,y[0]]))
#     # print(([x, y[1]]))
#     # if i < len(y):
#     #print('y',x,y)
#     for i in range(len(y)):
#
#         sub = []
#         sub.extend([list_set[0][a],y[i]])
#     #print(sub)
#         temp.append(sub)
#         a+= 1
# print('temp', temp)
# elif len(list_set) == 2:
#     temp = []
#     for y in list_set[1:]:
#         for i in range(len(y)):
#             for x in list_set[0]:
#                 sub = []
#                 sub.extend([x,y[i]])
#                 # sub+= x + y[i]
#                 # + element
#                 # sub.extend([x, y[i]])
#
#                 # print(sub)
#                 temp.append(sub)
#     print('temp', temp)