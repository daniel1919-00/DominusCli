from datetime import datetime
import json
from os import path, sep as dirSep, linesep, getcwd
from typing import Dict, List
from commands import Commands
from common import printError, getUserName, parsePlaceholders, getCopyrightText, printOk
from schematicProcessor import process
from dominus import DominusCLI
from paths import PATH_CLI_ROOT, PATH_DOMINUS_PROJECT_ROOT
from pathlib import Path
import re

argList = []
for arg in Commands['generate']['arguments']:
    argList.append(arg["argument"])
argList.sort()

def autocomplete(cliSession: DominusCLI, arguments: List):
    return argList

def getCurrentModuleName(session: DominusCLI) -> Dict:
    currentModuleName = ''
    currentPath = getcwd()
    if 'Modules' in currentPath:
        pathParts = currentPath.split(dirSep)
        for index, part in enumerate(pathParts):
            if part == 'Modules':
                try:
                    currentModuleName = pathParts[index + 1]
                except IndexError:
                    pass
                break

    return currentModuleName


def run(session: DominusCLI, arguments = []):
    try:
        schematicName = str(arguments[0]).lower()

        schematicFilePath = path.join(PATH_CLI_ROOT, 'schematics', schematicName + '.json')

        if not path.exists(schematicFilePath):
            printError(f"Schematic definition not found: {schematicFilePath}!")
            return

        schematicConfig = None
        with open(schematicFilePath) as schematicFile:
            schematicConfig = json.load(schematicFile)

    except IndexError:
        printError(f"Invalid schematic!")
        return

    try:
        generatedItemName = arguments[1]
    except IndexError:
        if 'allowEmptyName' in schematicConfig and schematicConfig['allowEmptyName']:
            generatedItemName = ''
        else:
            printError(f"Invalid name passed!")
            return

    if 'nameValidCheck' in schematicConfig and re.search(schematicConfig['nameValidCheck'], generatedItemName) != None:
        printError(f"Invalid name passed! Only {schematicConfig['nameValidCheck']} characters are allowed!")
        return

    if 'nameFirstCharUpper' in schematicConfig and schematicConfig['nameFirstCharUpper']:
        generatedItemName = re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), generatedItemName, 1)

    currentPath = getcwd()
    if schematicName == 'module':
        moduleDest = path.join(currentPath, generatedItemName)
        if 'Modules' not in currentPath:
            moduleDest = path.join(currentPath, 'Modules', generatedItemName)

        if path.exists(moduleDest):
            printError(f"A module with the same name exists: {moduleDest}")
            return

    currentDateTime = datetime.now()

    appNamespaceCacheFilePath = path.join(PATH_CLI_ROOT, '.appNamespace')
    appNamespace = 'App'
    if not path.exists(appNamespaceCacheFilePath):
        if PATH_DOMINUS_PROJECT_ROOT == '' or not path.exists(path.join(PATH_DOMINUS_PROJECT_ROOT, '.env')):
            userSpecifiedNameSpace = input("Dominus project application namespace not set! Enter one now, or leave empty to use the default: App\\").strip().strip('\\')
            if userSpecifiedNameSpace != '':
                appNamespace = userSpecifiedNameSpace
        else:
            dominusEnvFile = Path(path.join(PATH_DOMINUS_PROJECT_ROOT, '.env')).read_text()
            match = re.search(r'APP_NAMESPACE="(.*)"', dominusEnvFile)

            if match:
                extractedString = match.group(1)
                if extractedString != '':
                    appNamespace = extractedString
        with open(appNamespaceCacheFilePath, "w") as appNamespaceCacheFile:
            appNamespaceCacheFile.write(appNamespace)
    else:
        appNamespace = Path(appNamespaceCacheFilePath).read_text()

    placeholders = {
        '{{sep}}': dirSep,
        '{{username}}': getUserName(),
        '{{currentDate}}': currentDateTime.strftime("%Y-%m-%d"),
        '{{currentTime}}': currentDateTime.strftime("%H:%M:%S"),
        '{{generatedItemName}}': generatedItemName,
        '{{moduleName}}': getCurrentModuleName(session),
        '{{appNamespace}}': appNamespace
    }
    copyrightText = parsePlaceholders(getCopyrightText(), placeholders)
    if copyrightText != '':
        copyrightText = f"{linesep}{copyrightText}{linesep}"
    placeholders['{{copyright}}'] = copyrightText

    if "requiredTemplatePlaceholders" in schematicConfig and schematicConfig["requiredTemplatePlaceholders"]:
        for requiredPlaceholder in schematicConfig["requiredTemplatePlaceholders"]:
            if not requiredPlaceholder in placeholders:
                if requiredPlaceholder == '{{moduleName}}':
                    printError('Not in a module directory! Check path.')
                else:
                    printError(f"Missing required placeholder: {requiredPlaceholder}!")
                return
            elif not placeholders[requiredPlaceholder]:
                printError(f"Missing required placeholder ({requiredPlaceholder}) value!")
                return

    try:
        process(
            session,
            [schematicConfig],
            placeholders,
            path.join(PATH_CLI_ROOT, 'schematics', 'templates'))
        printOk(f"Successfully generated item [{generatedItemName}] based on [{schematicName}] schematic.")
    except Exception as e:
        printError(e)
