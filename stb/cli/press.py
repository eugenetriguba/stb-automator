import click
from config_file import ConfigFile
from lirc.exceptions import LircdCommandFailureError

from stb.remote import Remote
from stb.utils import get_config_file


@click.command(short_help="Send IR signals")
@click.argument("key", required=True)
@click.option("-r", "--remote", default=None, help="The remote to press keys on.")
def press(key, remote):
    """
    Simulate a button press by sending an IR signal
    """
    if not remote:
        remote = get_config_file().get("lirc.remote")

    try:
        Remote(remote).press(key)
        click.secho(f"Emitted {key} successfully", fg="green")
    except LircdCommandFailureError as error:
        click.secho(f"Error while trying to transmit {key}: ", fg="red")
        print(error)
