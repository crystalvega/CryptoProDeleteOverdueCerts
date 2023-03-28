from os import path, getcwd, chdir
import PySimpleGUI as sg
import subprocess, os, shutil
import win32security
from winreg import *

registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)

user_info = win32security.LookupAccountName(None,os.getlogin())
sid = win32security.ConvertSidToStringSid(user_info[0])

def ParseCerts(text):
    if 'Subject' in text:
        CONFS = ['Subject', 'Not valid after', 'SHA1 Hash', 'Container']
    elif 'Субъект' in text:
        CONFS = ['Субъект', 'Истекает', 'SHA1 отпечаток', 'Контейнер']
    else:
        sg.Popup('Ошибка!\nВ системе не обнаружены ЭЦП.')
        exit()
    i = 0
    textformated = [[]]
    returnvalue = []
    textlines = text.split('\n')
    for line in textlines:
        if str(i+1)+'-------' in line:
            i+=1
            textformated.append([])
        line = line.split(' : ')
        if len(line) != 1:
            textformated[i].append(line)
    del textformated[0]
    for i, certs in enumerate(textformated):
        returnvalue.append([])
        for cert in certs:
            for conf in CONFS:
                if conf in cert[0]:
                    returnvalue[i].append(cert[1])
    for i in range(0, len(returnvalue)):
        if 'CN=' in returnvalue[i][0]:
            returnvalue[i][0] = returnvalue[i][0].split('CN=')[1]
        returnvalue[i][2] = returnvalue[i][2].split('  ')[0]
        if len(returnvalue[i]) > 3:
            if 'FAT12' in returnvalue[i][3]:
                returnvalue[i][3] = returnvalue[i][3].split('\\')[2].replace('.000','')
    return returnvalue

def GetCerts():
    global certp
    certp = CheckCryptoPro()
    cwd = getcwd()
    try:
        chdir(certp)
        result = subprocess.run(['certmgr.exe', '-list', '-verbose', '-store', 'uMy'], shell=True, capture_output=True, text=True, encoding='866').stdout
    except:
        sg.Popup('Произошла ошибка запуска ПО Крипто ПРО.')
        exit()
    chdir(cwd)
    parsecerts = ParseCerts(result)
    parsecertswithck = FindClosedContainer(parsecerts)
    return parsecertswithck

def CheckCryptoPro():
    if path.exists(r'C:\Program Files\Crypto Pro\CSP\csptest.exe'):
        certp = 'C:\Program Files\Crypto Pro\CSP'
    elif path.exists(r'C:\Program Files (x86)\Crypto Pro\CSP\csptest.exe'):
        certp = 'C:\Program Files (x86)\Crypto Pro\CSP'
    else:
        sg.Popup('Ошибка!\nПрограммное обеспечение Крипто ПРО не найдено.')
        exit()
    return certp

def FindCKInReg(nameck):
    try:
        rawKeyA = OpenKey(registry, "SOFTWARE\\WOW6432Node\\Crypto Pro\\Settings\\Users\\" + sid + "\\Keys\\" + nameck)
        CloseKey(rawKeyA)
        return "SOFTWARE\\WOW6432Node\\Crypto Pro\\Settings\\Users\\" + sid + "\\Keys\\" + nameck
    except:
        return None
    
def FindCKInFat(disk, nameck):
    if os.path.isdir(disk + ':\\' + nameck):
        return disk + ':\\' + nameck
    else:
        return None

def FindClosedContainer(certs):
    chdir(certp)
    datasaved = []
    returnvalue = []
    result = subprocess.run(['csptest.exe', '-keyset', '-enum_cont', '--verifycontext', '--fqcn'], shell=True, capture_output=True, text=True, encoding='866').stdout
    closedcon = result.split('\n')
    for cert in certs:
        if len(cert) < 4:
            returnvalue.append(None)
            datasaved.append('N')
        else:
            if '\\\\' in cert[3]:
                cert[3] = cert[3].replace('\\\\', '\\')
            for con in closedcon:
                if cert[3] in con:
                    if con.startswith('\\\\.\\REGISTRY\\'):
                        dir_ck = FindCKInReg(con.replace('\\\\.\\REGISTRY\\',''))
                        datasaved.append('R')
                    elif con.startswith('\\\\.\\FAT12'):
                        dir_ck = FindCKInFat(con.replace('\\\\.\\FAT12_','').split('\\')[0], cert[3] + '.000')
                        datasaved.append('F')
                    else:
                        dir_ck.append(None)
                        datasaved.append('N')
                    returnvalue.append(dir_ck)
                    break
                elif con == 'OK.':
                    returnvalue.append(None)
                    datasaved.append('N')
                    break

                    
    for i in range(0,len(certs)):
        if len(certs[i]) > 3:
            certs[i][3] = returnvalue[i]
            certs[i].append(datasaved[i])
        else:
            certs[i].append(returnvalue[i])
            certs[i].append(datasaved[i])
    return certs

def DeleteCKfromR(key1, key2=''):
    if key1 != None:
        if key2=="":
            currentkey = key1
        else:
            currentkey = key1+ "\\" +key2
        
        open_key = OpenKey(registry, key1 ,0,KEY_ALL_ACCESS)
        infokey = QueryInfoKey(open_key)
        for x in range(0, infokey[0]):
            subkey = EnumKey(open_key, 0)
            try:
                DeleteKey(open_key, subkey)
                print ("Removed %s\\%s " % ( key1, subkey))
            except:
                DeleteCKfromR(registry, currentkey, subkey )

    DeleteKey(open_key,"")
    open_key.Close()
    print("Removed %s" % (currentkey))
    
def DeleteCKfromF(folder):
    if folder != None:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                sg.Popup('Ошибка!\nНе удалось удалить "' + folder + '".')

def Delete(certs):
    chdir(certp)
    certserror =[]
    retvalue = True
    for cert in certs:
        if cert[3] == 'R':
            DeleteCKfromR(cert[2])
        if cert[3] == 'F':
            DeleteCKfromF(cert[2])
        ret = subprocess.run(['certmgr.exe', '-delete', '-thumbprint', cert[1]], shell=True, capture_output=True, text=True, encoding='866').returncode
        if ret != 0:
            certserror.append(cert)
            retvalue = False
    return retvalue, certserror
