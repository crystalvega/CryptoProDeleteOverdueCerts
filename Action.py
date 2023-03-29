import datetime
import PySimpleGUI as sg
import DateSelector

progname = 'CryptoPro Delete Overdue Certs'

def DateFrom():
    listof = [sg.Input(size=(4,4), key='fac1'), sg.Text("."), sg.Input(size=(4,4), key='fac2'), sg.Text("."), sg.Input(size=(8,4),key='fac3'), sg.Button('Выбрать')]
        
    layout = [[sg.Text("Введите дату до которой не требуется удалять")], [sg.Text("сертификаты в формате ДД.ММ.ГГГГ(опционально): ")], listof, [sg.Button("ОК")]]

    window = sg.Window(progname, layout, use_default_focus=False)
    
    while True:
        event, values = window.read()
        if event == "Выбрать":
            window.close()
            selectdate = DateSelector.popup_get_date()
            if selectdate != None:
                listof = [sg.Input(default_text=selectdate[1],size=(4,4), key='fac1'), sg.Text("."), sg.Input(default_text=selectdate[0],size=(4,4), key='fac2'), sg.Text("."), sg.Input(default_text=selectdate[2],size=(8,4),key='fac3'), sg.Button('Выбрать')]
                layout = [[sg.Text("Введите дату до которой не требуется удалять")], [sg.Text("сертификаты в формате ДД.ММ.ГГГГ(опционально): ")], listof, [sg.Button("ОК")]]
            window = sg.Window(progname, layout, use_default_focus=False)
        if event == sg.WIN_CLOSED:
            window.close()
            return 'E'
        if event == "ОК":
            window.close()
            val = [values['fac1'],values['fac2'],values['fac3']]
            try:
                datetime.date(val[2],val[1],val[0])
                return val
            except TypeError:
                return None

def NotFound():
    listof = [sg.Text("Не найдено ни одного сертификата для удаления!")]
        
    layout = [listof, [sg.Button("ОК")]]

    window = sg.Window(progname, layout)

    while True:
        event, values = window.read()
        if event == "ОК" or event == sg.WIN_CLOSED:
            window.close()
            break

def Success():
    listof = [sg.Text("Операция успешно завершена!")]
        
    layout = [listof, [sg.Button("ОК")]]

    window = sg.Window(progname, layout)

    while True:
        event, values = window.read()
        if event == "ОК" or event == sg.WIN_CLOSED:
            window.close()
            break

def Error(certs):
    listof = [sg.Text("Не удалось удалить следующие сертификаты: ")]
    for cert in certs:
        listof.append(sg.Text(cert[0]))
        
    layout = [listof, [sg.Button("ОК")]]

    window = sg.Window(progname, layout)

    while True:
        event, values = window.read()
        if event == "ОК" or event == sg.WIN_CLOSED:
            window.close()
            break

def Confirm(certsfordelete):
    listof = [[sg.Text("ВНИМАНИЕ! Будут удалены следующие сертификаты: ")]]
    for cert in certsfordelete:
        listof.append([sg.Text('- ' +cert[0])])
        
    layout = listof,[[sg.Button("Подтверждаю"), sg.Button("Отмена")]]

    window = sg.Window(progname, layout)

    while True:
        event, values = window.read()
        if event == "Отмена" or event == sg.WIN_CLOSED:
            window.close()
            return False
        if event == "Подтверждаю" :
            window.close()
            return True

def GetOldCerts(certlist, fromdate=None):
    datereturn = []
    if fromdate is not None:
        fromdate = datetime.date(int(fromdate[2]),int(fromdate[1]),int(fromdate[0]))
    today = datetime.date.today()
    for cert in certlist:
        unformdate = cert[2].split('/')
        anotherday = datetime.date(int(unformdate[2]), int(unformdate[1]), int(unformdate[0]))
        diff = anotherday - today
        if diff.days < 0:
            if fromdate is not None:
                if anotherday > fromdate:
                    datereturn.append((cert[0],cert[1], cert[3], cert[4]))
            else:
                datereturn.append((cert[0],cert[1], cert[3], cert[4]))
    return datereturn