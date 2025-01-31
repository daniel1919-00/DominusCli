from os import path, scandir
from paths import PATH_CLI_THEMES
from json import load as loadJson

currentTheme = {}

def getThemesList():
    themes = []
    with scandir(PATH_CLI_THEMES) as entries:
        for entry in entries:
            themes.append(entry.name.replace('.json', ''))
    return themes

def getCurrentTheme() -> dict:
    return currentTheme

def setTheme(themeName):
    with open(path.join(PATH_CLI_THEMES, themeName + '.json')) as themeFile:
        theme = loadJson(themeFile)
        currentTheme.update(theme)
    