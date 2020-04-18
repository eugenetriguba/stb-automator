import click
from config_file import ConfigFile, ParsingError

from stb.utils import exit_with_error_output, get_config_file_path, module_path


@click.group(short_help="Manipulate or see your configuration file")
@click.option(
    "-p", "--path", "custom_path", help="Absolute path to the configuration file"
)
@click.pass_context
def config(ctx, custom_path):
    try:
        if custom_path:
            ctx.obj = ConfigFile(custom_path)
        else:
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
        print(error)


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
    internal_config_path = module_path("config/config.original.ini")

    if ctx.obj.path == internal_config_path:
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
    internal_config_path = module_path("config/config.original.ini")

    if ctx.obj.path == internal_config_path:
        click.secho(
            "You're using the internal configuration file, can't reset.", fg="red"
        )
    else:
        ctx.obj.restore_original(original_file_path=internal_config_path)
        click.secho(
            "Configuration file has been restored to its original state.", fg="green"
        )


@config.command(short_help="Lookup what configuration path is currently being used")
@click.pass_context
def info(ctx):
    """Lookup what configuration path is currently being used."""
    print(f"Current configuration file path: {ctx.obj.path}")


@config.command(short_help="Setup the user's configuration folder at ~/.stb")
def setup():
    pass
