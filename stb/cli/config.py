import click
from config_file import ConfigFile, ParsingError

from stb.utils import exit_with_error_output, get_config_file_path


@click.group(short_help="Print configuration file")
@click.argument("key", required=False)
@click.argument("value", required=False)
@click.option(
    "-d",
    "--delete",
    help="Deletes an entire section or a single key. "
    "If there is no dot (.), it will assume you want to delete the "
    "section. Otherwise if you only want to delete a key, use "
    "'section.key'.",
)
@click.option(
    "-r",
    "--reset",
    is_flag=True,
    help="Restores the configuration file to its original state.",
)
@click.option(
    "-p", "--path", "custom_path", help="Absolute path to the configuration file"
)
def config(key, value, delete, reset, info, custom_path):
    """
    Modify or output the configuration file.
    When retrieving or setting a configuration value, it should be specified in a
    section.key format. e.g. 'video.source_pipeline' or 'lirc.remote'.
    \b
    KEY: The 'section.key' in the configuration file.
    VALUE: The value of a key in the configuration file.
    """
    try:
        if custom_path:
            config_file = ConfigFile(custom_path)
        else:
            config_file = ConfigFile(get_config_file_path())

        if reset:
            config_file.restore_original()
            print("Configuration file has been restored to its original state.")
            exit(0)

        if delete:
            config_file.delete(delete)
            print(f"{delete} was successfully deleted.")
            exit(0)

        if key and not value:
            print(config_file.get(key))
            exit(0)

        if value:
            config_file.set(key, value)
            exit(0)

        print(config_file.stringify())

    except ParsingError as error:
        exit_with_error_output(error)


@config.command(short_help="Lookup what configuration path is currently being used")
def info():
    print(f"Current configuration file path: {get_config_file_path()}")


@config.command(short_help="Setup the user's configuration folder at ~/.hc")
def setup():
    pass
