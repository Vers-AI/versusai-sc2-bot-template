# Adapted from: https://github.com/DrInfy/sharpy-sc2/blob/master/dummy_ladder_zip.py

import os
import shutil
import zipfile
from typing import Optional

from bot import CompetitiveBot as bot

# Ignore the annoying resource warning from importing sc2 when an SC2 instance isn't running.
import warnings
warnings.simplefilter("ignore", ResourceWarning)

root_dir = os.path.dirname(os.path.abspath(__file__))

# the name of the generated zip file
zip_archive_name = "bot.zip"

# the folder to put the zip file in
copy_zip_to_folder = "publish"

# the files to include in the zip file
files_and_directories_to_zip = [
    "ladderbots.json",  # generated when this script is run
    "sc2",
    "bot",
    "requirements.txt",
    "run.py",
]

# the template for the ladderbots.json file that will be generated
ladderbots_json_template = """{
    "Bots": {
        "[NAME]": {
            "Race": "[RACE]",
            "Type": "Python",
            "RootPath": "./",
            "FileName": "run.py",
            "Args": "-O",
            "Debug": true,
            "SurrenderPhrase": "(pineapple)"
        }
    }
}"""


def generate_ladderbots_json() -> str:
    return ladderbots_json_template.replace("[NAME]", bot.NAME).replace("[RACE]", str(bot.RACE).split(".")[1])


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


def create_ladder_zip():
    print(f"Creating ladder zip...")

    # Remove previous archive
    if os.path.isfile(os.path.join(copy_zip_to_folder, zip_archive_name)):
        print(f"{os.linesep}Deleting {os.path.join(copy_zip_to_folder, zip_archive_name)}")
        os.remove(os.path.join(copy_zip_to_folder, zip_archive_name))

    files_to_zip = []
    directories_to_zip = []

    f = open("ladderbots.json", "w+")
    f.write(generate_ladderbots_json())
    f.close()

    for file in files_and_directories_to_zip:
        if not os.path.exists(file):
            raise ValueError(f"'{file}' does not exist.")

        if os.path.isdir(file):
            directories_to_zip.append(file)
        else:
            files_to_zip.append(file)

    print(f"{os.linesep}Zipping {zip_archive_name}")
    zipf = zipfile.ZipFile(zip_archive_name, "w", zipfile.ZIP_DEFLATED)
    for file in files_to_zip:
        zipf.write(file)
    for directory in directories_to_zip:
        zipdir(directory, zipf)
    zipf.close()

    os.remove("ladderbots.json")

    if not os.path.exists(copy_zip_to_folder):
        os.mkdir(copy_zip_to_folder)

    shutil.move(zip_archive_name, os.path.join(copy_zip_to_folder, zip_archive_name))

    print(f"{os.linesep}Successfully created {os.path.join(copy_zip_to_folder, zip_archive_name)}")


def main():
    create_ladder_zip()


if __name__ == "__main__":
    main()
