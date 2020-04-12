import click

from stb.remote import Remote


@click.command(short_help="Send IR signals")
@click.argument("key", required=True)
@click.argument("remote", default="*")
def press(key, remote):
    """Simulate a button press by sending an IR signal"""
    result = Remote("sonifi-remote").press("key_power")
    if result.success:
        print(f"Emitted {key} successfully")
    else:
        print(f"Error while trying to transmit {key}")
