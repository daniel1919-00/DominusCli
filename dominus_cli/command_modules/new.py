from os import path, mkdir, getcwd, chdir
from common import printError, printInfo, runTerminalCommand, getConfigParam, promptWarning, promptOk, deleteTree, promptInfo
from dominusManifestProcessor import processManifest
from json import load as loadJson
from dominus import DominusCLI
from shutil import copytree


def run(session: DominusCLI, arguments = []):
    try:
        projectName = str(arguments[0]).strip()
    except IndexError:
        printError('Invalid project name!')
        return

    projectDir = path.join(getcwd(), projectName)
    if path.exists(projectDir):
        if promptWarning('A directory with the same name already exists! Copy framework files? Y/n: ').strip().lower() != 'y':
            return
    else:
        mkdir(projectDir)

    projectTempDir = path.join(projectDir, '_temp')

    if path.exists(projectTempDir):
        deleteTree(projectTempDir)

    copyDockerConfig = promptInfo("Copy default docker config as well? Y/n: ").strip().lower() == 'y'

    if copyDockerConfig:
        totalInstallationSteps = 4
    else:
        totalInstallationSteps = 3
    currentInstallationStep = 1
    
    printInfo(f'[{currentInstallationStep}/{totalInstallationSteps}] Downloading Dominus source files.')
    currentInstallationStep += 1
    runTerminalCommand(f'git clone {getConfigParam("frameworkRepositoryUrl")} "{projectTempDir}"', True)

    if not path.exists(path.join(projectTempDir, 'src')):
        printError('Failed to create project! Missing Dominus source files!')
        deleteTree(projectTempDir)
        return

    printInfo(f'[{currentInstallationStep}/{totalInstallationSteps}] Looking for download manifest.')
    currentInstallationStep += 1

    downloadManifestFilePath = path.join(projectTempDir, 'download-manifest.json')
    if not path.exists(downloadManifestFilePath):
        printError("Download manifest not found!")
        deleteTree(projectTempDir)
        return

    printInfo(f'[{currentInstallationStep}/{totalInstallationSteps}] Copying Dominus files.')
    currentInstallationStep += 1

    with open(downloadManifestFilePath) as downloadManifestFile:
        manifest = loadJson(downloadManifestFile)
        processManifest(manifest, projectDir, projectTempDir, False)

    if copyDockerConfig:
        printInfo(f"[{currentInstallationStep}/{totalInstallationSteps}] Copying docker files.")
        copytree(path.join(projectTempDir, 'docker'), path.join(projectDir, 'docker'), dirs_exist_ok=True)
        currentInstallationStep += 1

    deleteTree(projectTempDir)

    if promptOk("Success! Switch to the newly created project? Y/n: ").strip().lower() == 'y':
        chdir(projectDir)