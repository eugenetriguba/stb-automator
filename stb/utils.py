import os
from pathlib import Path

import click


def get_config_file_path() -> Path:
    """
    Retrieve the path to the configuration file.

    Retrieved in the following order:
      * STB_CONFIG_FILE_PATH if it exists.
      * User configuration file at ~/.stb/config.ini if it exists.
      * The default configuration file in the stb module.
    """
    user_config = Path("~/.stb/config.ini").expanduser()
    search_hierarchy = [
        os.environ.get("STB_CONFIG_FILE_PATH"),
        user_config if user_config.exists() else None,
        module_path("config/config.original.ini"),
    ]

    for path in search_hierarchy:
        if path:
            return Path(path)


def module_path(path: str) -> Path:
    """
    Finds the absolute path of a file relative to the stb package.
    
    :param path: The path of the file you're looking for, starting from root.
    :return: The absolute path of the file
    """
    return Path.joinpath(Path(__file__).parent, path).resolve()


def exit_with_error_output(error):
    """
    Exits the program with an exit status of 1 and
    prints out the error message in a red color.

    :param error: The error that occurred. 
                  This could be a string or anything 
                  that can be converted to a string.
    """
    click.secho(str(error), fg="red")
    exit(1)
