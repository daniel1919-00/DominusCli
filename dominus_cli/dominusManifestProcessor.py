from os import path, makedirs
import shutil

def processManifest(downloadManifest: dict, projectRootDir: str, frameworkSrc: str, updateFramework):
    for frameworkFile in downloadManifest["manifest"]:
        if updateFramework and not frameworkFile["update"]:
            continue

        srcPath = path.join(frameworkSrc, frameworkFile["path"])
        destPath = path.join(projectRootDir, frameworkFile["path"].replace('src/', ''))

        if frameworkFile["type"] == "dir":
            if not path.exists(destPath):
                makedirs(destPath)
            
            shutil.copytree(srcPath, destPath, dirs_exist_ok=True)
        else:
            shutil.copyfile(srcPath, destPath)

    with open(path.join(projectRootDir, 'version'), "w") as projectVersionFile:
        projectVersionFile.write(downloadManifest["version"])