import datetime
import PySimpleGUI as sg

def NotFound():
    listof = [sg.Text("Не найдено ни одного сертификата для удаления!")]
        
    layout = [listof, [sg.Button("ОК")]]

    window = sg.Window("Demo", layout)

    while True:
        event, values = window.read()
        if event == "ОК" or event == sg.WIN_CLOSED:
            window.close()
            break

def Success():
    listof = [sg.Text("Операция успешно завершена!")]
        
    layout = [listof, [sg.Button("ОК")]]

    window = sg.Window("Demo", layout)

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

    window = sg.Window("Demo", layout)

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

    window = sg.Window("CryptoDeleteOldCerts", layout)

    while True:
        event, values = window.read()
        if event == "Отмена" or event == sg.WIN_CLOSED:
            window.close()
            return False
        if event == "Подтверждаю" :
            window.close()
            return True

def GetOldCerts(certlist):
    datereturn = []
    today = datetime.date.today()
    for cert in certlist:
        unformdate = cert[2].split('/')
        anotherday = datetime.date(int(unformdate[2]), int(unformdate[1]), int(unformdate[0]))
        diff = anotherday - today
        if diff.days < 0:
            datereturn.append((cert[0],cert[1], cert[3], cert[4]))
    return datereturn