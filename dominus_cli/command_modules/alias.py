import json
from os import path, getcwd
from typing import List
from commands import Commands, constructCommandAliasMap
from common import printError, printInfo, printOk, printWarning, replaceDirSeparatorWithOs
from tabulate import tabulate
from datetime import datetime
from dominus import DominusCLI
from paths import PATH_CLI_ROOT
from dominusUserConfig import getUserConfig, updateUserConfig

def run(session: DominusCLI, arguments: List = []):
    existingAliases = getUserConfig().get('existingAliases')
    defaultAliasDesc = True
    newAlias = True

    if '--export' in arguments:
        try:
            exportPath = replaceDirSeparatorWithOs(arguments[arguments.index('--export') + 1].strip())
            if exportPath == '':
                exportPath = getcwd()
        except IndexError:
            exportPath = getcwd()

        exportFilePath = path.join(exportPath, f'Dominus CLI - aliases export {datetime.now().strftime("%d-%m-%Y %H_%M_%S")}.json')
        with open(exportFilePath, 'w') as exportFile:
            json.dump(existingAliases, exportFile)

        if path.exists(exportFilePath):
            printOk(f'Aliases successfully exported to: {exportFilePath}')
        else:
           printError(f'Failed to export aliases!') 
        return
    elif '--import' in arguments:
        newAlias = False
        try:
            importFilePath = replaceDirSeparatorWithOs(arguments[arguments.index('--import') + 1].strip())
        except IndexError:
            importFilePath = ''

        if importFilePath == '' or not path.exists(importFilePath):
            printError(f"Invalid import file: {importFilePath}")
            return

        foundDuplicates = []
        with open(importFilePath) as importedAliasesFile:
            importedAliases = json.load(importedAliasesFile)
            for importedAlias in importedAliases:
                importedAliasDef = importedAliases[importedAlias]

                if importedAlias in existingAliases:
                    importedAliasDef["name"] = importedAlias
                    foundDuplicates.append(importedAliasDef)
                    continue

                existingAliases[importedAlias] = importedAliasDef
                Commands[importedAlias] = importedAliasDef
        
        if foundDuplicates:
            printWarning("The file was imported successfully, however the following duplicates where omitted:")
            tableData = []
            for duplicate in foundDuplicates:
                tableData.append([
                    duplicate["name"],
                    duplicate['description'],
                    duplicate['command']
                ])
            printWarning(tabulate(tableData, ["ALIAS", "DESCRIPTION", "COMMAND"], tablefmt="github"))
        else:
            printOk("Aliases imported successfully!")
    else:
        try:
            alias = arguments[0]

            if alias[:1] == '--':
                printError("Alias names can not start with '--'!")
                return

            arguments.pop(0)
        except IndexError:
            alias = ''

    if not arguments:
        arguments.append('--list')

    if '--list' in arguments:
        tableData = []
        for alias in existingAliases:
            aliasInfo = existingAliases[alias]
            tableData.append([
                alias,
                aliasInfo['description'],
                aliasInfo['command']
            ])

        printInfo(tabulate(tableData, ["ALIAS", "DESCRIPTION", "COMMAND"], tablefmt="github"))
        return

    if '--remove' in arguments:
        newAlias = False
        if not alias:
            printError("Specify the alias to be removed! Usage: alias <alias name> --remove")

        if not alias in existingAliases:
            printError(f'Alias "{alias}" not found!')
            return  

        if input(f"Permanently remove alias \"{alias}\"? Y/n: ").strip().lower() != 'y':
            return

        del existingAliases[alias]
        del Commands[alias]
        printWarning('Alias permanently removed!')
    elif '--description' in arguments:
        aliasDescArgPos = arguments.index('--description') + 1

        try:
            aliasDescription = arguments[aliasDescArgPos]
        except IndexError:
            printError("Custom description argument (-description) found but no custom description has been set!")
            return

        arguments.pop(aliasDescArgPos)
        arguments.pop(arguments.index('--description'))
        defaultAliasDesc = False
    else:
        aliasDescription = 'User Alias'

    if '--rename' in arguments:
        try:
            renamedAliasName = arguments[arguments.index('--rename') + 1]
        except IndexError:
            printError("Specify the alias to be renamed!")
            return

        session.parseInput(f"alias {alias} --change -n {renamedAliasName}")
        return
    elif '--change' in arguments:
        newAlias = False
        arguments.pop(arguments.index('--change'))
        changed = False

        if not alias:
            printError("Specify the alias to be changed!")

        if not alias in existingAliases:
            printError(f"Alias '{alias}' not found!")
            return  

        if '--name' in arguments:
            changed = True
            aliasRenameArgPos = arguments.index('--name') + 1

            try:
                newAliasName = arguments[aliasRenameArgPos]
                arguments.pop(aliasRenameArgPos)
            except IndexError:
                printError("Specify the new alias name!")
                return

            arguments.pop(arguments.index('--name'))

            rename = True
            if newAliasName in existingAliases:
                if input(f"Alias '{newAliasName}' already exists! Rename and overwrite? Y/n: ").strip().lower() != 'y':
                    rename = False
            if rename:
                existingAliases[newAliasName] = existingAliases.pop(alias)
                Commands[newAliasName] = Commands.pop(alias)
                alias = newAliasName

        if '--command' in arguments:
            changed = True
            arguments.pop(arguments.index('--command'))

            if not arguments:
                printError("Specify the new alias command!")
                return

            newCmd = ' '.join(arguments).replace('"', '"\\"').replace("'", "'\\'")
            existingAliases[alias]['command'] = newCmd
            Commands[alias]['command'] = newCmd

        if not defaultAliasDesc and existingAliases[alias]['description'] != aliasDescription:
            changed = True
            existingAliases[alias]['description'] = aliasDescription
            Commands[alias]['description'] = aliasDescription

        if not changed:
            printError("Nothing to change! Use the --name/--description/--command positional arguments to change the name, description and command respectively!")
            return
        printOk(f"Alias '{alias}' has been updated!")

    if newAlias: 
        if not alias:
            printError("Specify the alias name! Usage: alias <alias name> <options>")
            return

        if alias in existingAliases:
            if input(f"Alias '{alias}' already exists! Overwrite? Y/n: ").strip().lower() != 'y':
                return

        if not arguments:
            printError("Alias has no command to execute!")
            return

        try:
            aliasCommandDef = {
                'description': aliasDescription,
                'command': ' '.join(arguments).replace('"', '"\\"').replace("'", "'\\'"),
                'isAlias': True,
                'aliases': [],
                'arguments': [],
                'examples': []
            }
        except IndexError:
            printError("Missing alias command!")
            return
        
        existingAliases[alias] = aliasCommandDef
        Commands[alias] = aliasCommandDef

        printOk(f"Alias '{alias}' successfully created!")

    updateUserConfig(getUserConfig())
    
    constructCommandAliasMap()