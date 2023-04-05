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
            if selectdate == None:
                selectdate = ['','','']
            listof = [sg.Input(default_text=selectdate[1],size=(4,4), key='fac1'), sg.Text("."), sg.Input(default_text=selectdate[0],size=(4,4), key='fac2'), sg.Text("."), sg.Input(default_text=selectdate[2],size=(8,4),key='fac3'), sg.Button('Выбрать')]
            layout = [[sg.Text("Введите дату после которой не требуется удалять")], [sg.Text("сертификаты в формате ДД.ММ.ГГГГ(опционально): ")], listof, [sg.Button("ОК")]]
            window = sg.Window(progname, layout, use_default_focus=False)
            
        if event == sg.WIN_CLOSED:
            window.close()
            return 'E'
        if event == "ОК":
            window.close()
            val = [values['fac1'],values['fac2'],values['fac3']]
            try:
                datetime.date(int(val[2]),int(val[1]),int(val[0]))
                return val
            except TypeError:
                return None
            except ValueError:
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
        
def Edit(certs):
    certlist = []
    for index,cert in enumerate(certs):
        certlist.append(str(index+1) +'. (До ' + cert[2] + ") " + cert[0])
    text = [sg.Text('Выберите сертификаты, которые нужно убрать из списка:',size=(80, 2), font='Lucida', justification='center')]
    layout=[text,
            [sg.Listbox(values=certlist,select_mode='multiple', key='fac', size=(100,20))],
        [sg.Button('Убрать из списка', font=('Times New Roman',12))]]

    win = sg.Window(progname,layout)
    
    while True:
        event, values = win.read()
        if event == "Убрать из списка":
            win.close()
            retcert = []
            delcert = []
            for val in values['fac']:
                delcert.append(certs[int(val.split('. ')[0])-1])
            for cert in certs:
                if cert not in delcert:
                    retcert.append(cert)
            return retcert, certs
        if event == sg.WIN_CLOSED:
            win.close()
            return None

def Confirm(certsfordelete, allcerts=None):
    listof = [[sg.Text("ВНИМАНИЕ! Будут удалены следующие сертификаты: ")]]
    if allcerts is None:
        for cert in certsfordelete:
            listof.append([sg.Text('- (До ' +cert[2] + ') ' + cert[0])])
    else:
        for cert in allcerts:
            listof.append([sg.Text('- (До ' +cert[2] + ') ' + cert[0])])
        
    layout = listof,[[sg.Button("Подтверждаю"), sg.Button("Редактировать"), sg.Button("Отмена")]]

    window = sg.Window(progname, layout)

    while True:
        event, values = window.read()
        if event == "Отмена" or event == sg.WIN_CLOSED:
            window.close()
            return None
        if event == "Редактировать":
            window.close()
            try:
                certsfordelete, ac = Edit(certsfordelete)
            except TypeError:
                return None
            return Confirm(ac, certsfordelete)
        if event == "Подтверждаю" :
            window.close()
            try:
                if allcerts == None:
                    return certsfordelete
                else:
                    return allcerts
            except UnboundLocalError:
                return None

def GetOldCerts(certlist, fromdate):
    datereturn = []
    if fromdate is not None:
        today = datetime.date(int(fromdate[2]),int(fromdate[1]),int(fromdate[0]))
    else:
        today = datetime.date.today()
    for cert in certlist:
        unformdate = cert[2].split('/')
        anotherday = datetime.date(int(unformdate[2]), int(unformdate[1]), int(unformdate[0]))
        diff = anotherday - today
        if diff.days < 0:
            datereturn.append(cert)
    return datereturn