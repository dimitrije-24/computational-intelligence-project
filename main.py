import random
from typing import List

array = [['1','.','.','.'],['.','.','.','.'],['.','.','4','.'],['.','.','.','.']]

def initialize(num_on_board):
    return [[random.random() < 0.25 for _ in range(int(num_on_board/4))] for _ in range(int(num_on_board/4.0))]

solution = initialize(16)

def stampaj(niz):
    for i in range(4):
        for j in range(4):
            print(array[i][j],end=' ')
        print('\n')

stampaj(array)

def stampaj_modifikacija(niz):
    for i in range(4):
        for j in range(4):
            if array[i][j] == '.' and solution[i][j]:
                print('X',end=' ')
            else:
                print(array[i][j],end=' ')
        print('\n')

stampaj_modifikacija(array)