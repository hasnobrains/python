# -*- coding: utf-8 -*-

from pywebio.input import put_button, put_text, put_tabs, put_html, \
        put_scrollable, put_table, put_select
from pywebio.output import use_scope
from pywebio.pin import pin_wait_change
from pywebio import start_server
from functools import partial

dates_list = []
rep_dt = '1900-01-01'


def unused_list():
    #   Сюда надо скармливать записи без адресов
    useless_list = [[6, 'f'], [7, 'j']]
    return useless_list


def GoodPoints(date):
    #   Сюда надо скармилвать хорошие записи
    if date == '2021-10-07':
        goodPointsList = [[1, 'a'], [2, 'b']]
    else:
        goodPointsList = [[3, 'c'], [4, 'd']]
    return goodPointsList


def used_list():
    used_list_base = GoodPoints(rep_dt)
    for i in used_list_base:
        i.append(put_button("Find",
                            onclick=partial(ButtonClickFind, id=i[0])))
    return used_list_base


def ButtonClickUpdate():
    #   Сюда надо скармливать html карты на опред. дату
    file = 'Яндекс.html'
    with open(file, 'r', encoding='UTF-8') as f:
        html = f.read()
    with use_scope('map', clear=True):
        put_html(html)
    Main_Table()


def ButtonClickFind(id):
    #  Тут должно быть взаимодействие с картой
    #  по подсветке нужной точки
    put_text("You click button with id: %s" % (id))


@use_scope('mainTbl', clear=True)
def Main_Table():
    put_tabs([
            {'title': 'Heat map', 'content':
                [put_text("Report date: " + rep_dt),
                 put_scrollable(
                     put_table(used_list(),
                               header=['Type', 'Source', '']),
                     height=250,
                     keep_bottom=True),
                 put_select("date",
                            label="Select Date to show",
                            options=dates_list),
                 put_button("Show",
                            onclick=ButtonClickUpdate,
                            color='success',
                            outline=True)]},
            {'title': 'No Geo List',
             'content': put_table(unused_list(),
                                  header=['Type', 'Source'])}])


def get_dates():
    global dates_list
    #  Сюда надо скармливать список доступных исторических дат
    dates_list = ['2021-10-07', '2021-10-06', '2021-10-05']
    return dates_list


def app():
    global rep_dt
    get_dates()
    #    Здесь надо вставить максимальную дату из входных данных
    rep_dt = '2021-10-07'

    #   Сюда надо скармливать html карты
    with open(r"./127.0.0.1.html", 'r', encoding='UTF-8') as f:
        html = f.read()

    with use_scope('map', clear=True):
        put_html(html)

    Main_Table()

    while True:
        new_date = pin_wait_change(['date'])
        if new_date['name'] == 'date':
            #   Сюда мы сохраняем выбранную дату
            rep_dt = new_date['value']


if __name__ == '__main__':
    start_server(app, debug=True, port='44315')
