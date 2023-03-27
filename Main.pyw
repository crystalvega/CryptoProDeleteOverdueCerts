import CertMgr
import Action
from command_runner.elevate import elevate


def Main():
    certslist = CertMgr.GetCerts()
    certsfordelete = Action.GetOldCerts(certslist)
    if Action.Confirm(certsfordelete):
        e, certs = CertMgr.Delete(certsfordelete)
        if not e:
            Action.Error(certs)
    print(1)

if __name__ == "__main__":
    elevate(Main)