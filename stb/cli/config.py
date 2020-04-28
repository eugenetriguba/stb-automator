from pathlib import Path
from shutil import copyfile

import click
from config_file import ConfigFile, ParsingError

from stb.utils import (
    STB_INTERNAL_CONFIG_FILE,
    STB_USER_CONFIG_FILE,
    STB_USER_CONFIG_FOLDER,
    exit_with_error_output,
    get_config_file_path,
)


@click.group(short_help="Manipulate or see your configuration file")
@click.pass_context
def config(ctx, custom_path):
    try:
        ctx.obj = ConfigFile(get_config_file_path())
    except ParsingError as error:
        exit_with_error_output(error)


@config.command(short_help="Print out a section or key")
@click.argument("key")
@click.pass_context
def get(ctx, key):
    """
    Output a section or key of the configuration file.
    \b
    KEY: The 'section.key' in the configuration file.
    """
    try:
        print(ctx.obj.get(key))
    except ParsingError as error:
        exit_with_error_output(error)


@config.command(short_help="Set a key to a value")
@click.argument("key")
@click.argument("value")
@click.pass_context
def set(ctx, key, value):
    """
    Modify a key in the configuration file.
    \b
    KEY: The 'section.key' in the configuration file.
    VALUE: The value to set a key in the configuration file.
    """
    if ctx.obj.path == STB_INTERNAL_CONFIG_FILE:
        print("You're using the internal configuration path, which cannot be edited.")
        print("Run `stb config setup` instead to setup your user configuration file.")
    else:
        ctx.obj.set(key, value)
        click.secho("Successfully set {key} to {value}", fg="green")


@config.command(short_help="Print the configuration file")
@click.pass_context
def output(ctx):
    """Print the configuration file."""
    print(ctx.obj.stringify())


@config.command(short_help="Deletes an entire section or a single key")
@click.pass_context
def delete(ctx, key):
    """
    Deletes an entire section or a single key.

    If there is no dot (.), it will assume you want to delete the section.
    Otherwise if you only want to delete a key, use a 'section.key' syntax.
    """
    try:
        ctx.obj.delete(key)
        click.secho(f"{key} was successfully deleted.", fg="green")
    except ValueError as error:
        exit_with_error_output(error)


@config.command(short_help="Restores the configuration file to its original state")
@click.pass_context
def reset(ctx):
    """Restores the configuration file to its original state."""
    if ctx.obj.path == STB_INTERNAL_CONFIG_FILE:
        click.secho(
            "You're using the internal configuration file, can't reset.", fg="red"
        )
    else:
        ctx.obj.restore_original(original_file_path=STB_INTERNAL_CONFIG_FILE)
        click.secho(
            "Configuration file has been restored to its original state.", fg="green"
        )


@config.command(short_help="Lookup what configuration path is currently being used")
@click.pass_context
def info(ctx):
    """Lookup what configuration path is currently being used."""
    if Path(ctx.obj.path) == STB_INTERNAL_CONFIG_FILE:
        print(
            "You're using the internal configuration file that is in the package. "
            "If you'd like to setup your own user configuration that you can "
            "modify, run `stb config setup`."
        )
        exit(0)

    print(f"Current configuration file path: {ctx.obj.path}")


@config.command(short_help="Setup the user's configuration folder at ~/.stb")
def setup():
    if STB_USER_CONFIG_FILE.exists():
        print(
            f"You already have your configuration file setup at {STB_USER_CONFIG_FILE}"
        )
        exit(0)

    if not STB_USER_CONFIG_FOLDER.exists():
        STB_USER_CONFIG_FOLDER.mkdir()

    copyfile(STB_INTERNAL_CONFIG_FILE, STB_USER_CONFIG_FILE)
    click.secho(
        f"Successfully setup your user configuration file at {STB_USER_CONFIG_FILE}",
        fg="green",
    )
