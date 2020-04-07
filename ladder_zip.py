# Source: https://github.com/lladdy/chance-sc2/blob/master/ladder_zip.py

import os
import shutil

import zipfile
from typing import Tuple, List, Optional

import subprocess

# Adapted from https://github.com/DrInfy/sharpy-sc2/blob/master/dummy_ladder_zip.py

root_dir = os.path.dirname(os.path.abspath(__file__))


class LadderZip:
    archive: str
    files: List[str]

    def __init__(self, archive_name: str, race: str):
        self.name = archive_name
        self.race = race
        self.archive = archive_name + ".zip"
        self.files = [
            "chance",
            "sharpy-sc2/sharpy",
            "sharpy-sc2/python-sc2/sc2",
            "sharpy-sc2/sc2pathlibp",
            "sharpy-sc2/jsonpickle",
            "requirements.txt",
            "version.txt",
            "config.py",
            "config.ini",
            "ladderbots.json",
            "run.py",
        ]

    def pre_zip(self):
        """ Override this as needed, actions to do before creating the zip"""
        pass

    def post_zip(self):
        """ Override this as needed, actions to do after creating the zip"""
        pass


def zipdir(path: str, ziph: zipfile.ZipFile, remove_path: Optional[str] = None):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            if "__pycache__" not in root:
                path_to_file = os.path.join(root, file)
                if remove_path:
                    ziph.write(path_to_file, path_to_file.replace(remove_path, ""))
                else:
                    ziph.write(path_to_file)


def update_version_txt():
    try:
        commit_hash = subprocess.check_output("git rev-parse --short HEAD", stderr=subprocess.STDOUT).decode().strip()
        commit_date = (
            subprocess.check_output("git log -1 --date=short --pretty=format:%cd", stderr=subprocess.STDOUT)
            .decode()
            .strip()
        )

        with open("version.txt", mode="w") as file:
            file.write(commit_date + "\n")
            file.write(commit_hash)
            print(f"Updated version.txt with: {commit_date} {commit_hash}")
    except Exception:
        print(f"unable to update version.txt. Using previous values instead (if found).")


def create_ladder_zip(archive_zip: LadderZip):
    update_version_txt()
    print()

    archive_name = archive_zip.archive

    bot_specific_paths = archive_zip.files

    # Remove previous archive
    if os.path.isfile(archive_name):
        print(f"Deleting {archive_name}")
        os.remove(archive_name)

    files_to_zip = []
    directories_to_zip = []
    files_to_delete = []

    archive_zip.pre_zip()

    for file in bot_specific_paths:
        if not os.path.exists(file):
            raise ValueError(f"'{file}' does not exist.")

        if os.path.isdir(file):
            directories_to_zip.append(file)
        else:
            files_to_zip.append(file)

    print()
    print(f"Zipping {archive_name}")
    zipf = zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED)
    for file in files_to_zip:
        zipf.write(file)
    for directory in directories_to_zip:
        zipdir(directory, zipf)
    zipf.close()

    print()
    for file in files_to_delete:

        if os.path.isdir(file):
            print(f"Deleting directory {file}")
            # os.rmdir(file)
            shutil.rmtree(file)
        else:
            print(f"Deleting file {file}")
            os.remove(file)

    if not os.path.exists("publish"):
        os.mkdir("publish")

    shutil.move(archive_name, os.path.join("publish", archive_name))
    archive_zip.post_zip()

    print(f"\nSuccessfully created {os.path.join('publish', archive_name)}")


def main():
    create_ladder_zip(LadderZip("Chance", "Random"))


if __name__ == "__main__":
    main()
