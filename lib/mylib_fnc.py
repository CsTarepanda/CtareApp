import os

def date_parse(date_string):
    from datetime import datetime, date
    date_ar = [int(x) for x in date_string.split("/")]
    date_len = len(date_ar)
    now_year = date.today().year
    if date_len == 0:
        return None
    elif date_len == 1:
        import calendar
        return date(
                now_year,
                date_ar[0],
                calendar.monthrange(now_year, date_ar[0])[1]
                )
    elif date_len == 2:
        return date(now_year, date_ar[0], date_ar[1])
    elif date_len == 3:
        return date(date_ar[0], date_ar[1], date_ar[2])
    elif date_len == 4:
        return datetime(
                date_ar[0],
                date_ar[1],
                date_ar[2],
                date_ar[3])
    elif date_len == 5:
        return datetime(
                date_ar[0],
                date_ar[1],
                date_ar[2],
                date_ar[3],
                date_ar[4])
    elif date_len == 6:
        return datetime(
                date_ar[0],
                date_ar[1],
                date_ar[2],
                date_ar[3],
                date_ar[4],
                date_ar[5])


COLOR_SPACE = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]


def _color_get_place(byte_1):
    if byte_1 == 0xff:
        return 5
    for index, i in enumerate(COLOR_SPACE):
        if i > byte_1:
            return index - (1 if byte_1 - COLOR_SPACE[index - 1] <= i - byte_1 else 0)


def color(byte_3):
    if byte_3%0xa0a0a == 0x80808:
        return 232 + int((byte_3 - 0x080808) / 0xa0a0a)
    pos = 16
    for i in range(3):
        pos += _color_get_place(byte_3 & 0xff) * 6**i
        byte_3 >>= 8
    return pos


def mkcl(color_num):
    return "[38;5;{}m".format(color_num)


def mkclb(color_num):
    return "[48;5;{}m".format(color_num)


def cstr(string, col):
    return "{0}{1}{2}[0m".format(col[0], col[1], string)


def cprint(string, col):
    print(cstr(string, col))


def inprint(string):
    os.system('echo "[s"; tput cuu1; tput il1')
    print(string)
    os.system('tput rc')
