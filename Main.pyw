import CertMgr
import Action
from command_runner.elevate import elevate


def Main():
    certslist = CertMgr.GetCerts()
    datefrom = Action.DateFrom()
    if datefrom != 'E':
        certsfordelete = Action.GetOldCerts(certslist, datefrom)
        if len(certsfordelete) == 0:
            Action.NotFound()
        else:
            if Action.Confirm(certsfordelete):
                e, certs = CertMgr.Delete(certsfordelete)
                if not e:
                    Action.Error(certs)
                else:
                    Action.Success()

if __name__ == "__main__":
    elevate(Main)