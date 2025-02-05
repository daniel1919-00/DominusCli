import json
from os import path, mkdir
from paths import PATH_CLI_ROOT, PATH_DEFAULT_SAVE_DATA
from pathlib import Path
from common import getAbsolutePath, printInfo, printOk

_savedConfigPathFilePath = path.join(PATH_DEFAULT_SAVE_DATA, '.savedConfigPath')
cliConfigurationDone = path.exists(_savedConfigPathFilePath)
_savedDataDirPath = PATH_DEFAULT_SAVE_DATA
_defaultConfiguration = {
    "existingAliases": {},
    "appNamespace": "App",
    "currentTheme": "default"
}
_configCache = None

def getConfigFilePath(dirPath):
    configFilePath = getAbsolutePath(dirPath)
    return path.join(configFilePath, 'dominus_cli_config.json')

def getUserConfig():
    global _configCache

    if not _configCache:
        if cliConfigurationDone:
            _savedDataDirPath = getAbsolutePath(Path(_savedConfigPathFilePath).read_text())
            configFilePath = getConfigFilePath(_savedDataDirPath)
            if path.exists(configFilePath):
                with open(configFilePath, "r") as savedConfigFile:
                    savedConfig = json.load(savedConfigFile)
                    config = {**_defaultConfiguration, **savedConfig}
                    return config
        else:
            return _defaultConfiguration

    return _configCache

def getSavedDataDirPath():
    return _savedDataDirPath

def updateUserConfig(newConfig):
    _configCache = getUserConfig()
    _configCache.update(newConfig)

    with open(getConfigFilePath(getSavedDataDirPath()), "w") as configFileCache:
        json.dump(_configCache, configFileCache)

def updateSavedConfigPath(savedConfigDirPath):
    global _savedDataDirPath

    _savedDataDirPath = getAbsolutePath(savedConfigDirPath)
    with open(_savedConfigPathFilePath, "w") as savedConfigPathFile:
            savedConfigPathFile.write(_savedDataDirPath)

def setupUserConfiguration():
    global _configCache
    
    printInfo("Preparing dominus cli for first time use, please configure the following:")
    
    savedDataDirPath = input(f"Please specify the path to where the cli will store and retrieve user saved configurations.\nThis directory can then later be stored in a git repository.\n\nRelative paths are evaluated from the script run directory: {PATH_CLI_ROOT}/\nSaved configurations directory (Leave empty for default): ").strip()
    if not savedDataDirPath:
        savedDataDirPath = getSavedDataDirPath()
    else:
        if path.exists(getConfigFilePath(savedDataDirPath)):
            updateSavedConfigPath(savedDataDirPath)
            printOk("Loaded existing configuration!")
            return

    appNamespace = input("Please specify the project application namespace, this ensures that any generated boilerplate classes have proper namespace.\n App namespace (Leave empty for default): ").strip()
    if not appNamespace:
        appNamespace = _defaultConfiguration.get('appNamespace')

    newConfig = {
        "appNamespace": appNamespace
    }

    print(f"The following configuration will be saved to the specified Saved configurations directory: {getAbsolutePath(savedDataDirPath)}")
    print(json.dumps(newConfig, indent=4))
    ok = input("Is this ok? Y/N: ").strip().lower()
    
    if ok == 'y':
        updateSavedConfigPath(savedDataDirPath)
        mkdir(path.join(getSavedDataDirPath(), 'templates'))
        updateUserConfig(newConfig)
    else:
        setupUserConfiguration()
        