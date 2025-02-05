from dominus import DominusCLI
from common import printError, printOk, getAbsolutePath
from dominusUserConfig import updateUserConfig, updateSavedConfigPath
from os import path

def run(session: DominusCLI, arguments = []):
    try:
        setConfiguration = arguments[0]
    except IndexError:
        printError("Invalid argument passed")
        return
    
    try:
        setConfigurationValue = arguments[1]
    except IndexError:
        printError("Invalid argument value passed")
        return
    
    if setConfiguration == 'namespace':
        setConfigurationValue = setConfigurationValue.strip()
        if setConfigurationValue != '':
            appNamespace = setConfigurationValue
        else:
            printError("Invalid application namespace given!")
            return

        updateUserConfig({"appNamespace": appNamespace})
        
        printOk(f"New application namespace set: {appNamespace}")
        return
        
    elif setConfiguration == 'dominus-config-dir':
        if setConfigurationValue != '':
            dominusConfigDirPath = setConfigurationValue
            if not path.exists(dominusConfigDirPath):
                printError("Could not access the given Dominus configuration directory path!")
                return
            
            updateSavedConfigPath(dominusConfigDirPath)
            updateUserConfig({"savedDataDirPath": dominusConfigDirPath})

            printOk(f"New configuration directory set: {getAbsolutePath(dominusConfigDirPath)}")
        else:
            printError("Invalid Dominus configuration directory path given!")
            return