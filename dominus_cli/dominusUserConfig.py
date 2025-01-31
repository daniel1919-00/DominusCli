import json
from os import path
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

def loadConfigFile(configFilePath):
    if cliConfigurationDone:
        configFilePath = path.join(Path(_savedConfigPathFilePath).read_text(), 'dominus_cli_config.json')
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
    _configCache.update(newConfig)
    with open(path.join(_configCache.get('savedDataDirPath'), 'dominus_cli_config.json'), "w") as configFileCache:
        json.dump(_configCache, configFileCache)

def updateSavedConfigPath(savedDataDirPath):
    with open(_savedConfigPathFilePath, "w") as savedConfigPathFile:
            savedConfigPathFile.write(savedDataDirPath)

def setupUserConfiguration():
    global _configCache
    
    print("Preparing dominus cli for first time use, please configure the following:")
    
    savedDataDirPath = input(f"Please specify the path to where the cli will store and retrieve user saved configurations.\nThis directory can then later be stored in a git repository.\nSaved configurations directory: ").strip()
    if not savedDataDirPath:
        savedDataDirPath = _configCache.get('savedDataDirPath')
    else:
        if path.exists(path.join(savedDataDirPath, 'dominus_cli_config.json')):
            _configCache = loadConfigFile(savedDataDirPath)
            updateSavedConfigPath(savedDataDirPath)
            print("Loaded existing configuration.")
            return

    appNamespace = input("Please specify the project application namespace, this ensures that any generated boilerplate classes have proper namespace.").strip()
    if not appNamespace:
        appNamespace = _configCache.get('appNamespace')

    newConfig = {
        "savedDataDirPath": savedDataDirPath,
        "appNamespace": appNamespace
    }

    print(f"The following configuration will be saved to the specified Saved configurations directory: {savedDataDirPath}")
    print(newConfig)
    ok = input("Is this ok? Y/N: ").strip().lower()
    
    if ok == 'y':
        updateSavedConfigPath(savedDataDirPath)
        updateUserConfig(newConfig)
    else:
        setupUserConfiguration()
        