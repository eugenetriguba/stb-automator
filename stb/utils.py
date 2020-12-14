import os
from pathlib import Path

import click
from config_file import ConfigFile


def module_path(path: str) -> Path:
    """
    Finds the absolute path of a file relative to the stb package.

    Args:
        path: The path of the file you're looking for, starting from root.
    
    Returns:
        The absolute path of the file
    """
    return Path.joinpath(Path(__file__).parent, path).resolve()


STB_CONFIG_FILE_ENV_VAR = os.environ.get("STB_CONFIG_FILE_PATH")
STB_USER_CONFIG_FOLDER = Path("~/.stb/").expanduser()
STB_USER_CONFIG_FILE = Path("~/.stb/config.toml").expanduser()
STB_INTERNAL_CONFIG_FILE = module_path("config/config.original.toml")


def get_config_file() -> ConfigFile:
    """
    Retrieve the path to the configuration file.

    Retrieved in the following order:
      * The STB_CONFIG_FILE_PATH enviroment variable if it exists.
      * User configuration file at ~/.stb/config.toml if it exists.
      * The default configuration file in the stb module.

    Returns:
        A ConfigFile for that path that was found first in the search heirarchy.
    """
    search_hierarchy = [
        STB_CONFIG_FILE_ENV_VAR,
        STB_USER_CONFIG_FILE if STB_USER_CONFIG_FILE.exists() else None,
        STB_INTERNAL_CONFIG_FILE,
    ]

    for path in search_hierarchy:
        if path:
            return ConfigFile(path)


def exit_with_error_output(error):
    """
    Exits the program with an exit status of 1 and
    prints out the error message in a red color.

    :param error: The error that occurred. This could be
        a string or anything that can be converted to a string.
    """
    click.secho(str(error), fg="red")
    exit(1)
