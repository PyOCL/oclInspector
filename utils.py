import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def print_info(data):
    for row in data:
        if type(row[2]) == list:
            print("{0:<2} {1:<20}: {2: >50}".format(row[0], row[1], row[2][0]))
            for i in range(1, len(row[2])):
                print("{0:<2} {1:<20}: {2: >50}".format("", "", row[2][i]))
        else:
            print("{0:<2} {1:<20}: {2: >50}".format(*row))
