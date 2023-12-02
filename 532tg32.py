# import requests
#
# flag = True
# response = requests.get("https://stepik.org/media/attachments/course67/3.6.3/699991.txt")
# while flag:
#     response = requests.get(f"https://stepik.org/media/attachments/course67/3.6.3/{response.text}")
#     print(response.text)
#     print(response.text[0:2])
#     print(1)
#     if response.text[0:2] == "We":
#         flag = False
# print(response.text)
#
#
#
# with open("test_qe.txt", "r") as data:
#     dict_data = dict()
#     for i in range(1,12):
#         dict_data.setdefault(str(i), [])
#     list_data = data.readlines()
#     for line in list_data:
#         list_strip = line.strip().split()
#         print(list_strip)
#         dict_data[list_strip[0]] += [int(list_strip[-1])]
#
# with open("answ.txt", "w") as data_answ:
#     for i in range(1,12):
#         if dict_data.get(str(i)) == []:
#             print(dict_data.get(str(1)))
#             data_answ.write(f"{i} -\n")
#         else:
#             data_answ.write(f"{i} {sum(dict_data[str(i)]) / len(dict_data[str(i)])}\n")
#
# print(dict_data)
#
#
# n = int(input())
# dict_move = {"север": 0, "запад": 0, "юг": 0, "восток": 0}
# for i in range(n):
#     list_coord = input().split(" ")
#     dict_move[list_coord[0]] += int(list_coord[1])
#
# print(dict_move["восток"] - dict_move["запад"], dict_move["север"] - dict_move["юг"])
#
#
# n = int(input())
# dict_word = dict()
# for _ in range(n):
#     dict_word.setdefault(input().lower(), True)
#
# list_word = []
# set_word = set()
# count_string = int(input())
# for _ in range(count_string):
#     list_word += input().lower().split()
#
# set_word = set(list_word)
#
#
# for key in dict_word.keys():
#     if key in set_word:
#         set_word.discard(key)
#
# for word in set_word:
#     print(word)
#
#
#
#
# # encode_symbol = input()
# # decode_symbol = input()
# # encode_str = input()
# # decode_str = input()
# # len_encode = len(encode_symbol)
# #
# # encode = dict()
# # decode = dict()
# #
# # answ1 = ""
# # answ2 = ""
# #
# # for i in range(len_encode):
# #     encode.setdefault(encode_symbol[i], decode_symbol[i])
# #     decode.setdefault(decode_symbol[i], encode_symbol[i])
# #
# # for symbol in encode_str:
# #     answ1 += encode[symbol]
# #
# # for symbol in decode_str:
# #     answ2 += decode[symbol]
# #
# # print(answ1)
# # print(answ2)
#
#
#
#
# # n = int(input())
# # list_game = [[] for i in range(n)]
# # dict_game = dict()
# # for i in range(n):
# #     list_game[i] = input().split(";")
# #
# # for i in range(n):
# #     for j in range(0,3,2):
# #         if not(dict_game.get(list_game[i][j], False)):
# #             dict_game.setdefault(list_game[i][j], {"match": 1, "win": 0, "drow": 0, "lose": 0, "all_point": 0})
# #         else:
# #             dict_game[list_game[i][j]]["match"] += 1
# #     if int(list_game[i][1]) > int(list_game[i][3]):
# #         dict_game[list_game[i][0]]["win"] += 1
# #         dict_game[list_game[i][0]]["all_point"] += 3
# #         dict_game[list_game[i][2]]["lose"] += 1
# #     elif int(list_game[i][1]) < int(list_game[i][3]):
# #         dict_game[list_game[i][2]]["win"] += 1
# #         dict_game[list_game[i][2]]["all_point"] += 3
# #         dict_game[list_game[i][0]]["lose"] += 1
# #     else:
# #         dict_game[list_game[i][0]]["drow"] += 1
# #         dict_game[list_game[i][2]]["drow"] += 1
# #         dict_game[list_game[i][0]]["all_point"] += 1
# #         dict_game[list_game[i][2]]["all_point"] += 1
# #
# # for kay, value in dict_game.items():
# #     print(f"{kay}:{value['match']} {value['win']} {value['drow']} {value['lose']} {value['all_point']}")
# #
# #
# #
# #
# n = int(input())
# a = [[0 for j in range(n)] for i in range(n)]
#
#
# class SpiralNum:
#     def __init__(self, n, a):
#         self.n = n
#         self.end_prog = 1
#         self.count_insert = n
#         self.count_insert_time = n
#         self.cord_x = 0
#         self.cord_y = 0
#         self.list_matrix = a
#         self.count_insert_end = n ** 2
#
#
#     def end_func(self):
#         for i in range(n):
#             rt = self.list_matrix[i]
#             print(*rt)
#
#
#     def right_fill(self):
#         if self.end_prog != 1:
#             self.cord_x += 1
#         if self.end_prog == self.count_insert_end+1:
#             return self.end_func()
#         while self.count_insert_time != 0:
#             self.list_matrix[self.cord_y][self.cord_x] = self.end_prog
#             self.end_prog += 1
#             self.cord_x += 1
#             self.count_insert_time -= 1
#
#         self.cord_x -= 1
#         self.count_insert -= 1
#         self.count_insert_time = self.count_insert
#         self.down_fill()
#
#
#     def down_fill(self):
#         self.cord_y += 1
#         if self.end_prog == self.count_insert_end+1:
#             return self.end_func()
#         while self.count_insert_time != 0:
#             self.list_matrix[self.cord_y][self.cord_x] = self.end_prog
#             self.end_prog += 1
#             self.cord_y += 1
#             self.count_insert_time -= 1
#
#         self.cord_y -= 1
#         self.count_insert_time = self.count_insert
#         self.left_fill()
#
#
#     def left_fill(self):
#         self.cord_x -= 1
#         if self.end_prog == self.count_insert_end+1:
#             return self.end_func()
#         while self.count_insert_time != 0:
#             self.list_matrix[self.cord_y][self.cord_x] = self.end_prog
#             self.end_prog += 1
#             self.cord_x -= 1
#             self.count_insert_time -= 1
#
#         self.cord_x += 1
#         self.count_insert -= 1
#         self.count_insert_time = self.count_insert
#         self.up_fill()
#
#
#     def up_fill(self):
#         self.cord_y -= 1
#         if self.end_prog == self.count_insert_end+1:
#             return self.end_func()
#         while self.count_insert_time != 0:
#             self.list_matrix[self.cord_y][self.cord_x] = self.end_prog
#             self.end_prog += 1
#             self.cord_y -= 1
#             self.count_insert_time -= 1
#
#         self.cord_y += 1
#         self.count_insert_time = self.count_insert
#         self.right_fill()
#
#
# SpiralNum(n, a).right_fill()
# #
# #
# #
# # # 1 2 3 4 5
# # # 16 17 18 19 6
# # # 15 24 25 20 7
# # # 14 23 22 21 8
# # # 13 12 11 10 9
# #
# #
# # # import copy
# # #
# # # a = input()
# # # lenght_matrix_j = 0
# # # list_of_matrix = []
# # # prom = []
# # # zero = 0
# # #
# # # while a != "end":
# # #     a = a.split(" ")
# # #     for i in a:
# # #         prom += [int(i)]
# # #     list_of_matrix += [prom]
# # #     prom = []
# # #     a = input()
# # #     lenght_matrix_j += 1
# # #
# # # lenght_matrix = len(list_of_matrix[0])
# # #
# # # copy_list_of_matrix = copy.deepcopy(list_of_matrix)
# # #
# # #
# # # for j in range(lenght_matrix):
# # #     for i in range(lenght_matrix_j):
# # #         ind_j = lambda j, zero: zero if j + 1 >= lenght_matrix else j + 1
# # #         ind_i = lambda i, zero: zero if i + 1 >= lenght_matrix_j else i + 1
# # #         copy_list_of_matrix[i][j] = list_of_matrix[i][ind_j(j, zero)] + list_of_matrix[i][
# # #             j - 1] + list_of_matrix[i - 1][j] + \
# # #                                     list_of_matrix[ind_i(i, zero)][j]
# # #
# # #
# # # for i in range(lenght_matrix_j):
# # #     rt = copy_list_of_matrix[i]
# # #     print(*rt)
