from common import printInfo, runTerminalCommand, getConfigParam, printError, printOk, promptInfo, printWarning, deleteTree
from os import path, getcwd
from json import load as loadJson
from pathlib import Path
from dominusManifestProcessor import processManifest
from dominus import DominusCLI

def run(session: DominusCLI, arguments = []):
    projectDir = getcwd()
    projectTempDir = path.join(projectDir, '_temp')
    projectVersionFile = path.join(projectDir, '.version')

    if path.exists(projectVersionFile):
        currentProjectVersion = Path(projectVersionFile).read_text()
    else:
        if not path.exists(projectDir, 'download-manifest.json'):
            printError("Command must be run in a Dominus project directory!")
            return
        else:
            currentProjectVersion = '0.0.0'
            Path(projectVersionFile).touch()

    totalInstallationSteps = 4
    currentInstallationStep = 1
    
    printInfo(f'[{currentInstallationStep}/{totalInstallationSteps}] Downloading Dominus source files.')
    currentInstallationStep += 1

    if path.exists(projectTempDir):
        deleteTree(projectTempDir)

    runTerminalCommand(f'git clone {getConfigParam("frameworkRepositoryUrl")} "{projectTempDir}"', True)

    if not path.exists(path.join(projectTempDir, 'src')):
        printError('Failed to update project! Missing Dominus source files!')
        deleteTree(projectTempDir)
        return

    printInfo(f'[{currentInstallationStep}/{totalInstallationSteps}] Looking for download manifest.')
    currentInstallationStep += 1

    downloadManifestFilePath = path.join(projectTempDir, 'download-manifest.json')
    if not path.exists(downloadManifestFilePath):
        printError("Download manifest not found!")
        deleteTree(projectTempDir)
        return

    printInfo(f'[{currentInstallationStep}/{totalInstallationSteps}] Checking for updated files.')
    currentInstallationStep += 1

    with open(downloadManifestFilePath) as downloadManifestFile:
        manifest = loadJson(downloadManifestFile)
        if manifest["version"] == currentProjectVersion:
            printOk("No updates found.")
        elif promptInfo(f"Update found. Dominus will update from from [v{currentProjectVersion}] to [v{manifest['version']}]. Continue? Y/n: ").strip().lower() == 'y':
            printInfo(f'[{currentInstallationStep}/{totalInstallationSteps}] Updating Dominus.')
            currentInstallationStep += 1
            processManifest(manifest, projectDir, projectTempDir, True)
            
            try:
                newProjectVersion = Path(projectVersionFile).read_text()
            except:
                printError(f"Dominus version could not be verified!")

            if newProjectVersion == manifest['version']:
                printOk(f"Dominus successfully updated from [v{currentProjectVersion}] to [v{manifest['version']}]")
                printWarning(f"Remember to run the command: composer dump-autoload")
            else:
                printError(f"Dominus version could not be verified!")
        else:
            printWarning("Update canceled.")
            
    deleteTree(projectTempDir)