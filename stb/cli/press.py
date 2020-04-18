import click

from stb.remote import Remote


@click.command(short_help="Send IR signals")
@click.argument("remote", required=True)
@click.argument("key", required=True)
def press(key, remote):
    """Simulate a button press by sending an IR signal"""
    result = Remote(remote).press(key)
    if result.success:
        click.secho(f"Emitted {key} successfully", fg="green")
    else:
        click.secho(f"Error while trying to transmit {key}", fg="red")
