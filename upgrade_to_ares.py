import os
import shutil
import re
import sys
from subprocess import run


def check_dependencies() -> None:
    """Check that required external tools are installed."""
    missing = []
    for cmd in ["git", "poetry"]:
        if shutil.which(cmd) is None:
            missing.append(cmd)
    
    if missing:
        print("Error: Missing required dependencies:")
        for cmd in missing:
            print(f"  - {cmd}")
        print("\nPlease install them and try again.")
        sys.exit(1)

HOOKS: list[str] = [
    "on_step",
    "on_start",
    "on_end",
    "on_building_construction_complete",
    "on_unit_created",
    "on_unit_destroyed",
    "on_unit_took_damage",
]

REQUIRED_DIRS: list[str] = [
    "ares-sc2",
    "scripts",
    ".github/workflows",
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
        with open(run_py_path, "r+", encoding="utf-8") as f:
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
                f.truncate()
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

        source_workflow_path = os.path.join(
            dest_directory, ".github", "workflows", "ladder_zip.yml"
        )
        dest_workflow_path = os.path.join(
            ".", ".github", "workflows", "ladder_zip.yml"
        )

        dest_directory_path = os.path.dirname(dest_workflow_path)
        os.makedirs(dest_directory_path, exist_ok=True)

        if os.path.exists(source_workflow_path):
            shutil.move(source_workflow_path, dest_workflow_path)
            print("Moved ladder_zip.yml successfully.")
        else:
            print("ladder_zip.yml not found in the destination directory.")

def convert_main_to_ares(
    main_py_path: str = os.path.join("bot", "main.py")
) -> None:
    """
    Tries to convert an existing python-sc2 style main.py into an ares-sc2 bot
    """
    if not os.path.exists(main_py_path):
        print(f"{main_py_path} not found, skipping ares conversion.")
        return

    with open(main_py_path, "r", encoding="utf-8") as f:
        source = f.read()

    original_source = source

    # 1) Replace sc2 BotAI import with ares AresBot
    source = re.sub(
        r"from\s+sc2\.bot_ai\s+import\s+BotAI",
        "from ares import AresBot",
        source,
    )

    # 2) Change base class BotAI -> AresBot on the main bot class
    source = re.sub(
        r"class\s+(\w+)\s*\(\s*BotAI\s*\)\s*:",
        r"class \1(AresBot):",
        source,
    )

    # 3) Extract the bot class name
    class_match = re.search(
        r"class\s+(?P<name>\w+)\s*\(\s*(?:AresBot|BotAI)\s*\)\s*:", source
    )
    class_name = class_match.group("name") if class_match else "MyBot"

    # 4) For each hook, add super(...) calls
    # We look for async defs inside the bot class and inject super calls
    # at the top of the function body if missing.
    def add_super_calls(text: str, cls_name: str) -> str:
        # Simple regex that matches async def hook inside a class.
        def repl(match: re.Match) -> str:
            indent = match.group("indent")
            name = match.group("name")
            args = match.group("args")
            body = match.group("body")

            # If there's already a super call, leave as-is.
            if "super(" in body:
                return match.group(0)

            # Build ares-style super call based on hook.[page:0]
            call = ""
            if name == "on_step":
                call = f"await super({cls_name}, self).on_step(iteration)\n"
            elif name == "on_start":
                call = f"await super({cls_name}, self).on_start()\n"
            elif name == "on_end":
                call = f"await super({cls_name}, self).on_end(result)\n"
            elif name == "on_building_construction_complete":
                call = (
                    f"await super({cls_name}, self)."
                    "on_building_construction_complete(unit)\n"
                )
            elif name == "on_unit_created":
                call = f"await super({cls_name}, self).on_unit_created(unit)\n"
            elif name == "on_unit_destroyed":
                call = f"await super({cls_name}, self).on_unit_destroyed(unit_tag)\n"
            elif name == "on_unit_took_damage":
                call = (
                    f"await super({cls_name}, self)."
                    "on_unit_took_damage(unit, amount_damage_taken)\n"
                )
            else:
                return match.group(0)

            super_line = indent + "    " + call
            new_body = super_line + body
            return (
                f"{indent}async def {name}({args}) -> None:\n{new_body}"
            )

        # Pattern:
        #   <indent>async def on_step(self, iteration: int) -> None:
        #   <indent>    ...
        hook_pattern = (
            r"(?P<indent>[ \t]*)async\s+def\s+"
            r"(?P<name>"
            + "|".join(HOOKS)
            + r")"
            r"\((?P<args>[^)]*)\)(?:\s*->\s*None)?:\s*\n"
            r"(?P<body>(?:(?P=indent)\s+.*\n)*)"
        )
        return re.sub(hook_pattern, repl, text)

    source = add_super_calls(source, class_name)

    if source != original_source:
        with open(main_py_path, "w", encoding="utf-8") as f:
            f.write(source)
        print(f"Converted {main_py_path} to use ares-sc2 patterns.")
    else:
        print(
            f"No changes made to {main_py_path}; "
            "existing code may already match ares patterns or "
            "did not match the conversion heuristics."
        )


def find_bot_file_from_run_py(run_py_path: str = "run.py") -> str | None:
    """
    Parse run.py to find the bot's main file by inspecting imports.
    Looks for patterns like:
        from bot import CompetitiveBot
        from bot.main import MyBot
    """
    if not os.path.exists(run_py_path):
        return None

    with open(run_py_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern 1: from <module> import <BotClass>
    # Pattern 2: from <module.submodule> import <BotClass>
    import_pattern = r"from\s+(?P<module>[\w.]+)\s+import\s+(?P<class>\w+)"

    for match in re.finditer(import_pattern, content):
        module = match.group("module")
        class_name = match.group("class")

        # Skip known non-bot imports
        if module in ("sc2", "sc2.main", "sc2.data", "sc2.client", 
                      "sc2.player", "sc2.protocol", "config", "argparse",
                      "asyncio", "logging", "aiohttp", "random"):
            continue

        # Try to resolve module to file path
        # Handle both package imports and direct file imports
        candidates = [
            f"{module.replace('.', '/')}.py",  # bot/main.py
        ]
        
        init_path = f"{module.replace('.', '/')}/__init__.py"
        if os.path.exists(init_path):
            candidates.append(init_path)
        
        # Also try simple module.py for top-level imports
        simple_path = f"{module}.py"
        if simple_path not in candidates:
            candidates.append(simple_path)

        for candidate in candidates:
            if os.path.exists(candidate):
                # If it's an __init__.py, check if it re-exports from a submodule
                if candidate.endswith("__init__.py"):
                    re_export = find_re_exported_file(candidate, class_name)
                    if re_export:
                        return re_export
                return candidate

    return None


def find_re_exported_file(init_path: str, class_name: str) -> str | None:
    """
    Check if __init__.py re-exports a class from a submodule.
    e.g., 'from .bot import CompetitiveBot' -> returns path to bot.py
    """
    with open(init_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match: from .<submodule> import <class_name>
    pattern = rf"from\s+\.(?P<submodule>\w+)\s+import\s+{class_name}"
    match = re.search(pattern, content)
    
    if match:
        submodule = match.group("submodule")
        init_dir = os.path.dirname(init_path)
        submodule_path = os.path.join(init_dir, f"{submodule}.py")
        if os.path.exists(submodule_path):
            return submodule_path
    
    return None


if __name__ == "__main__":
    check_dependencies()

    print("Cloning ares-sc2-template...")
    run(
        "git clone --recursive https://github.com/AresSC2/ares-sc2-bot-template",
        shell=True,
        check=True,
    )

    destination_directory = os.path.join("./", "ares-sc2-bot-template")
    print("Juggling around some files...")
    moves_files_and_dirs(destination_directory)

    print("Setting up ares")
    run("poetry install", shell=True, check=True)

    print("Modifying run.py")
    modify_run_py()

    print("Detecting bot file from run.py...")
    bot_file = find_bot_file_from_run_py()
    
    if bot_file:
        print(f"Found bot file: {bot_file}")
        convert_main_to_ares(bot_file)
    else:
        print("Could not auto-detect bot file. Checking common locations...")
        for path in [os.path.join("bot", "bot.py"), os.path.join("bot", "main.py"), "bot.py"]:
            if os.path.exists(path):
                print(f"Found bot file: {path}")
                convert_main_to_ares(path)
                break
        else:
            print("No bot file found. Please specify manually.")

    print("Cleaning up")
    shutil.rmtree(destination_directory, onerror=on_error)
