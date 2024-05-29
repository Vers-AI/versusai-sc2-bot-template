import os
import shutil

from subprocess import Popen, run

REQUIRED_DIRS: list[str] = [
    "ares-sc2",
    "scripts"
    ".github/workflows"
]

REQUIRED_FILES: list[str] = [
    "config.yml",
    "poetry.lock",
    "pyproject.toml",
]


def on_error(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat

    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def modify_run_py() -> None:
    run_py_path = os.path.join("./", "run.py")
    if os.path.exists(run_py_path):
        with open(run_py_path, "r+") as f:
            lines = f.readlines()
            # Check if the lines are already present
            if all("sys.path.append" not in line for line in lines):
                # Add the required lines at the beginning of the file
                lines.insert(0, "import sys\n")
                lines.insert(1, "sys.path.append('ares-sc2/src/ares')\n")
                lines.insert(2, "sys.path.append('ares-sc2/src')\n")
                lines.insert(3, "sys.path.append('ares-sc2')\n")

                # Move the file pointer to the beginning of the file
                f.seek(0)
                # Write the modified lines back to the file
                f.writelines(lines)
                print("Modified run.py successfully.")
    else:
        print("run.py not found in the destination directory.")


def moves_files_and_dirs(dest_directory: str) -> None:
    if os.path.exists(dest_directory):
        for dir_name in REQUIRED_DIRS:
            source_dir = os.path.join(dest_directory, dir_name)
            if os.path.exists(source_dir):
                dest_dir = os.path.join(".", dir_name)
                if os.path.exists(dest_dir):
                    shutil.rmtree(dest_dir, onerror=on_error)
                shutil.move(source_dir, dest_dir)

        for file_name in REQUIRED_FILES:
            source_file = os.path.join(dest_directory, file_name)
            if os.path.exists(source_file):
                dest_file = os.path.join(".", file_name)
                if os.path.exists(dest_file):
                    os.remove(dest_file)
                shutil.move(source_file, dest_file)

        source_workflow_path = os.path.join(dest_directory, ".github", "workflows", "ladder_zip.yml")
        dest_workflow_path = os.path.join(".", ".github", "workflows", "ladder_zip.yml")

        dest_directory_path = os.path.dirname(dest_workflow_path)
        os.makedirs(dest_directory_path, exist_ok=True)

        if os.path.exists(source_workflow_path):
            shutil.move(source_workflow_path, dest_workflow_path)
            print("Moved ladder_zip.yml successfully.")
        else:
            print("ladder_zip.yml not found in the destination directory.")


if __name__ == "__main__":
    print("Cloning ares-sc2-template...")
    run("git clone --recursive https://github.com/AresSC2/ares-sc2-bot-template", shell=True)

    destination_directory = os.path.join("./", "ares-sc2-bot-template")
    print("Juggling around some files...")
    moves_files_and_dirs(destination_directory)

    print("Setting up ares")
    run("poetry install", shell=True)

    print("Modifying run.py")
    modify_run_py()

    print("Cleaning up")
    shutil.rmtree(destination_directory, onerror=on_error)
