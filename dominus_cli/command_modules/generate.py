from datetime import datetime
import json
from os import path, sep as dirSep, linesep, getcwd
from typing import Dict, List
from commands import Commands
from common import printError, getUserName, parsePlaceholders, getCopyrightText, printOk
from schematicProcessor import process
from dominus import DominusCLI
from paths import PATH_CLI_ROOT
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
        commandArguments = Commands["generate"]["arguments"]
        found = False
        allowEmptyName = False
        for argDef in commandArguments:
            if schematicName == argDef["argument"]:
                found = True
                if 'allowEmptyName' in argDef and argDef['allowEmptyName']:
                    allowEmptyName = True
                break
        if not found:
            printError(f"Invalid schematic: {schematicName}")
            return
    except IndexError:
        printError(f"Invalid schematic!")
        return

    try:
        generatedItemName = arguments[1]
    except IndexError:
        if allowEmptyName:
            generatedItemName = ''
        else:
            printError(f"Invalid generated item name passed!")
            return

    generatedItemName = re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), generatedItemName, 1)
    currentPath = getcwd()

    if schematicName == 'module':
        moduleDest = path.join(currentPath, generatedItemName)
        if 'Modules' not in currentPath:
            moduleDest = path.join(currentPath, 'Modules', generatedItemName)

        if path.exists(moduleDest):
            printError(f"A module with the same name exists: {moduleDest}")
            return

    schematicFilePath = path.join(PATH_CLI_ROOT, 'schematics', schematicName + '.json')

    if not path.exists(schematicFilePath):
        printError(f"Schematic definition not found: {schematicFilePath}!")
        return

    with open(schematicFilePath) as schematicFile:
        schematicConfig = json.load(schematicFile)
        currentDateTime = datetime.now()

        placeholders = {
            '{{sep}}': dirSep,
            '{{username}}': getUserName(),
            '{{currentDate}}': currentDateTime.strftime("%Y-%m-%d"),
            '{{currentTime}}': currentDateTime.strftime("%H:%M:%S"),
            '{{generatedItemName}}': generatedItemName,
            '{{moduleName}}': getCurrentModuleName(session)
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
        