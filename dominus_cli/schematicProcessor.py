from os import makedirs, path, sep as sepDir, getcwd
import pathlib
from common import importPythonModule, printError, printOk, replaceDirSeparatorWithOs, runTerminalCommand, parsePlaceholders
from dominus import DominusCLI
    
def alterTemplatePlaceholders(templatePlaceholders, alterations):
    for alterationConfig in alterations:
        placeholder = alterationConfig["placeholder"]
        
        if alterationConfig['type'] == 'replace':
            templatePlaceholders[placeholder] = templatePlaceholders[placeholder].replace(alterationConfig["from"].replace('{{sep}}', sepDir), alterationConfig["to"].replace('{{sep}}', sepDir))
        elif alterationConfig['type'] == 'add':
            templatePlaceholders[placeholder] = parsePlaceholders(alterationConfig['value'], templatePlaceholders)

    return templatePlaceholders

def make(session: DominusCLI, config, templatePlaceholders, templatesPath):
    destination = getcwd()
    
    if "template" in config:
        templateFile = path.join(templatesPath, config["template"])
    else:
        templateFile = ''

    if "destinationPathAbsolute" in config:
        destination = parsePlaceholders(replaceDirSeparatorWithOs(config["destinationPathAbsolute"]), templatePlaceholders)
    elif "destinationPath" in config:
        destPath = parsePlaceholders(replaceDirSeparatorWithOs(config["destinationPath"]), templatePlaceholders)
        if path.basename(path.normpath(destination)) != path.basename(destPath):
            destination = path.join(destination, destPath)
    
    if "alterTemplatePlaceholders" in config:
        templatePlaceholders = alterTemplatePlaceholders(templatePlaceholders, config["alterTemplatePlaceholders"])


    if config["type"] == 'custom':
        importPythonModule('schematics.client.%s' % (config["pythonModule"])).run(None, templatePlaceholders, session, templateFile)

    elif config["type"] == 'command':
        commandResponse = runTerminalCommand(parsePlaceholders(config["command"], templatePlaceholders))
        
        if commandResponse.error:
            printError(commandResponse.error)
            raise Exception("Generate command interrupted due to error!")
        
        if "pythonModule" in config:
            importPythonModule('schematics.client.%s' % (config["pythonModule"])).run(commandResponse, templatePlaceholders, session, templateFile)

        printOk(commandResponse.output)
    else:
        if not path.exists(destination):
            pathlib.Path(destination).mkdir(parents=True, exist_ok=True)

        if "name" in config:
            makeName = parsePlaceholders(config["name"], templatePlaceholders)
        else:
            makeName = ''

        if config["type"] == 'file':
            with open(path.join(destination, makeName), "w") as file:
                fileContents = ''

                if templateFile:
                    with open(templateFile) as templateFile:
                        fileContents = parsePlaceholders(templateFile.read(), templatePlaceholders)

                file.write(fileContents)
        else:
            destination = path.join(destination, makeName)
            makedirs(destination, exist_ok=True)
    
    return destination


def process(session: DominusCLI, makeConfigurations, templatePlaceholders, templatesPath):
    for makeConfig in makeConfigurations:
        makeDestDir = make(session, makeConfig, templatePlaceholders, templatesPath)
        
        if makeDestDir is None:
            break

        if "make" in makeConfig:
            makeConfigs = makeConfig["make"]
            if makeConfigs:
                for index, value in enumerate(makeConfigs):
                    makeConfigs[index]["destinationPath"] = makeDestDir
                process(session, makeConfigs, templatePlaceholders, templatesPath)
