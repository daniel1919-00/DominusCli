from os import path, scandir
from paths import PATH_CLI_ROOT, PATH_CLI_THEMES
from shutil import copyfile
from json import load as loadJson

currentTheme = None
currentThemeFilePath = path.join(PATH_CLI_ROOT, 'theme.json')
defaultThemeFilePath = path.join(PATH_CLI_THEMES, 'default.json')

class Theme :
    name = ''
    promptColor = ''
    printInfoColor = ''
    printOkColor = ''
    printWarningColor = ''
    printErrorColor = ''
    printCmdOutputColor = ''
    helpHeaderColor = ''
    helpColor = ''
    ls_dirColor = ''
    ls_fileColor = ''

    def __init__(self, themeConfig: dict) -> None:
        self.name = themeConfig["name"]
        self.promptColor = themeConfig["promptColor"]
        self.printInfoColor = themeConfig["printInfoColor"]
        self.printOkColor = themeConfig["printOkColor"]
        self.printWarningColor = themeConfig["printWarningColor"]
        self.printErrorColor = themeConfig["printErrorColor"]
        self.printCmdOutputColor = themeConfig["printCmdOutputColor"]
        self.helpColor = themeConfig["helpColor"]
        self.ls_dirColor = themeConfig["ls_dirColor"]
        self.ls_fileColor = themeConfig["ls_fileColor"]

def getCurrentTheme() -> Theme:
    return currentTheme

def reloadTheme():
    global currentTheme
    with open(currentThemeFilePath) as themeFile:
        try:
            currentTheme = Theme(loadJson(themeFile))
        except KeyError:
            print(f"Theme file out of date. Using default theme. Remove or update the {currentThemeFilePath} theme config to fix this.")
            with open(defaultThemeFilePath) as defaultThemeFile:
                currentTheme = Theme(loadJson(defaultThemeFile))

if not path.exists(currentThemeFilePath):
    copyfile(defaultThemeFilePath, currentThemeFilePath)

def getThemesList():
    themes = []
    with scandir(PATH_CLI_THEMES) as entries:
        for entry in entries:
            themes.append(entry.name.replace('.json', ''))
    return themes

def getTheme(name: str) -> Theme | None:
    themePath = path.join(PATH_CLI_THEMES, name + '.json')
    if not path.exists(themePath):
        return None

    with open(themePath) as themeFile:
        return Theme(loadJson(themeFile))