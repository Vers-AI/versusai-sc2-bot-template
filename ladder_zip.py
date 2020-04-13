# Adapted from: https://github.com/DrInfy/sharpy-sc2/blob/master/dummy_ladder_zip.py

import os
import shutil

import zipfile
from typing import Optional

root_dir = os.path.dirname(os.path.abspath(__file__))


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

    zip_archive_name = "bot.zip"
    copy_zip_to_folder = "publish"

    files_and_directories_to_zip = [
        "python-sc2/sc2",
        "bot",
        "requirements.txt",
        "ladderbots.json",
        "run.py",
    ]

    # Remove previous archive
    if os.path.isfile(os.path.join(copy_zip_to_folder, zip_archive_name)):
        print(f"{os.linesep}Deleting {os.path.join(copy_zip_to_folder, zip_archive_name)}")
        os.remove(os.path.join(copy_zip_to_folder, zip_archive_name))

    files_to_zip = []
    directories_to_zip = []

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

    if not os.path.exists(copy_zip_to_folder):
        os.mkdir(copy_zip_to_folder)

    shutil.move(zip_archive_name, os.path.join(copy_zip_to_folder, zip_archive_name))

    print(f"{os.linesep}Successfully created {os.path.join(copy_zip_to_folder, zip_archive_name)}")


def main():
    create_ladder_zip()


if __name__ == "__main__":
    main()
