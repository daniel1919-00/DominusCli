import json
from os import path
from paths import PATH_CLI_ROOT
from pathlib import Path
from common import printInfo, promptInfo, printOk

cliConfigurationDone = False
cliDefaultSaveDataDirPath = path.join(PATH_CLI_ROOT, 'savedData')
savedConfigPathFilePath = path.join(cliDefaultSaveDataDirPath, '.savedConfigPath')

def updateSavedConfigPath(savedDataDirPath):
    with open(savedConfigPathFilePath, "w") as savedConfigPathFile:
            savedConfigPathFile.write(savedDataDirPath)

def loadConfigFile(configFilePath):
    global cliConfigurationDone
    
    if path.exists(savedConfigPathFilePath):
        configFilePath = path.join(Path(savedConfigPathFilePath).read_text(), 'dominus_cli_config.json')
        if path.exists(configFilePath):
            cliConfigurationDone = True
            with open(configFilePath, "r") as configFile:
                return json.load(configFile)
    else:
        return {
            "savedDataDirPath": cliDefaultSaveDataDirPath, 
            "existingAliases": {},
            "appNamespace": "App"
        }

configCache = loadConfigFile(cliDefaultSaveDataDirPath)

def getConfig():
    global configCache
    return configCache

def updateConfig(newConfig):
    global configCache
    configCache.update(newConfig)
    with open(path.join(configCache.get('savedDataDirPath'), 'dominus_cli_config.json'), "w") as configFileCache:
        json.dump(configCache, configFileCache)

def setupUserConfiguration():
    global configCache
    printInfo("Preparing dominus cli for first time use, please configure the following:")
    savedDataDirPath = promptInfo(f"Please specify the path to where the cli will store and retrieve user saved configurations.\nThis directory can then later be stored in a git repository.\nSaved configurations directory: ").strip()
    if not savedDataDirPath:
        savedDataDirPath = configCache.get('savedDataDirPath')
    else:
        if path.exists(path.join(savedDataDirPath, 'dominus_cli_config.json')):
            configCache = loadConfigFile(savedDataDirPath)
            updateSavedConfigPath(savedDataDirPath)
            printOk("Loaded existing configuration.")
            return

    appNamespace = promptInfo("Please specify the project application namespace, this ensures that any generated boilerplate classes have proper namespace.").strip()
    if not appNamespace:
        appNamespace = configCache.get('appNamespace')

    newConfig = {
        "savedDataDirPath": savedDataDirPath,
        "appNamespace": appNamespace
    }

    printInfo(f"The following configuration will be saved to the specified Saved configurations directory: {savedDataDirPath}")
    print(newConfig)
    ok = promptInfo("Is this ok? Y/N: ").strip().lower()
    
    if ok == 'y':
        updateSavedConfigPath(savedDataDirPath)
        updateConfig(newConfig)
    else:
        setupUserConfiguration()
        