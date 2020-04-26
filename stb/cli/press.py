import click
from config_file import ConfigFile

from stb.remote import Remote
from stb.utils import get_config_file_path


@click.command(short_help="Send IR signals")
@click.argument("key", required=True)
@click.option("-r", "--remote", default=None, short_help="The remote to press keys on.")
def press(key, remote):
    """
    Simulate a button press by sending an IR signal

    """
    if not remote:
        config = ConfigFile(get_config_file_path())
        remote = config.get("lirc.remote")

    result = Remote(remote).press(key)
    if result.success:
        click.secho(f"Emitted {key} successfully", fg="green")
    else:
        click.secho(f"Error while trying to transmit {key}", fg="red")
