from os import chdir
from common import printError, replaceDirSeparatorWithOs
from dominus import DominusCLI

def run(session: DominusCLI, arguments = []):
    try:
        requiredPath = replaceDirSeparatorWithOs(str(arguments[0]).strip())
    except IndexError:
        return

    try:
        chdir(requiredPath)
    except PermissionError:
        printError("Permission denied!")
    except FileNotFoundError:
        printError("Directory not found!")
    except:
        printError("Could not change path!")