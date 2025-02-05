import json
from os import path, mkdir
from paths import PATH_CLI_ROOT
from pathlib import Path

cliDefaultSaveDataDirPath = path.join(PATH_CLI_ROOT, 'savedData')
_savedConfigPathFilePath = path.join(cliDefaultSaveDataDirPath, '.savedConfigPath')
cliConfigurationDone = path.exists(_savedConfigPathFilePath)
_defaultConfiguration = {
    "savedDataDirPath": cliDefaultSaveDataDirPath, 
    "existingAliases": {},
    "appNamespace": "App",
    "currentTheme": "default"
}
_configCache = None

def getConfigFilePath(savedDataDirPath):
    if path.isabs(savedDataDirPath):
        configFilePath = savedDataDirPath
    else:
        configFilePath = path.join(PATH_CLI_ROOT, savedDataDirPath)
    
    return path.join(configFilePath, 'dominus_cli_config.json')

def loadConfigFile(configFilePath):
    if cliConfigurationDone:
        configFilePath = getConfigFilePath(Path(_savedConfigPathFilePath).read_text())
        if path.exists(configFilePath):
            with open(configFilePath, "r") as savedConfigFile:
                savedConfig = json.load(savedConfigFile)
                config = {**_defaultConfiguration, **savedConfig}
                return config
    else:
        return _defaultConfiguration.copy()

def getUserConfig():
    global _configCache

    if not _configCache:
        _configCache = loadConfigFile(cliDefaultSaveDataDirPath)

    return _configCache

def updateUserConfig(newConfig):
    _configCache = getUserConfig()
    _configCache.update(newConfig)

    with open(getConfigFilePath(_configCache.get('savedDataDirPath')), "w") as configFileCache:
        json.dump(_configCache, configFileCache)

def updateSavedConfigPath(savedDataDirPath):
    with open(_savedConfigPathFilePath, "w") as savedConfigPathFile:
            savedConfigPathFile.write(savedDataDirPath)

def setupUserConfiguration():
    global _configCache
    
    print("Preparing dominus cli for first time use, please configure the following:")
    
    savedDataDirPath = input(f"Please specify the path to where the cli will store and retrieve user saved configurations.\nThis directory can then later be stored in a git repository.\n\nRelative paths are evaluated from the script run directory: {PATH_CLI_ROOT}/\nSaved configurations directory: ").strip()
    if not savedDataDirPath:
        savedDataDirPath = _defaultConfiguration.get('savedDataDirPath')
    else:
        if path.exists(getConfigFilePath(savedDataDirPath)):
            _configCache = loadConfigFile(savedDataDirPath)
            updateSavedConfigPath(savedDataDirPath)
            print("Loaded existing configuration!")
            return

    appNamespace = input("Please specify the project application namespace, this ensures that any generated boilerplate classes have proper namespace.\n App namespace: ").strip()
    if not appNamespace:
        appNamespace = _defaultConfiguration.get('appNamespace')

    newConfig = {
        "savedDataDirPath": savedDataDirPath,
        "appNamespace": appNamespace
    }

    mkdir(path.join(savedDataDirPath, 'templates'))

    print(f"The following configuration will be saved to the specified Saved configurations directory: {savedDataDirPath}")
    print(newConfig)
    ok = input("Is this ok? Y/N: ").strip().lower()
    
    if ok == 'y':
        updateSavedConfigPath(savedDataDirPath)
        updateUserConfig(newConfig)
    else:
        setupUserConfiguration()
        