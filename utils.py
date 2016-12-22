import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def print_info(data):
    for row in data:
        if type(row[2]) == list:
            print("{0:<2} {1:<40}: {2: >40}".format(row[0], row[1], row[2][0]))
            for i in range(1, len(row[2])):
                print("{0:<2} {1:<40}: {2: >40}".format("", "", row[2][i]))
        else:
            print("{0:<2} {1:<40}: {2: >40}".format(*row))

def format_byte(val):
    assert type(val) == int

    if val < 1024:
        return "{0}B".format(val)
    elif val < 1024 * 1024:
        return "{0:.2f}KB".format(float(val) / 1024)
    elif val < 1024 * 1024 * 1024:
        return "{0:.2f}MB".format(float(val) / 1024 / 1024)
    elif val < 1024 * 1024 * 1024 * 1024:
        return "{0:.2f}GB".format(float(val) / 1024 / 1024/ 1024)
    else:
        return "{0:.2f}TB".format(float(val) / 1024 / 1024/ 1024 / 1024)
