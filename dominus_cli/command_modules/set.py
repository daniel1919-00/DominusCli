from dominus import DominusCLI
from common import printError, printOk
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
    elif setConfiguration == 'template-extension-path':
        if setConfigurationValue != '':
            templateExtensionPath = setConfigurationValue
            if not path.exists(templateExtensionPath):
                printError("Could not access the given templates extension path!")
                return
            
            updateUserConfig({"templateExtensionPath": templateExtensionPath})
            printOk(f"Templates will be extended using .json files found in this path: {templateExtensionPath}")
        else:
            printError("Invalid template extension path given!")
            return
        
    elif setConfiguration == 'dominus-config-dir':
        if setConfigurationValue != '':
            dominusConfigDirPath = setConfigurationValue
            if not path.exists(dominusConfigDirPath):
                printError("Could not access the given Dominus configuration directory path!")
                return
            updateSavedConfigPath(dominusConfigDirPath)
            updateUserConfig({"savedDataDirPath": dominusConfigDirPath})
        else:
            printError("Invalid Dominus configuration directory path given!")
            return