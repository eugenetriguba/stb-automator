import click

from stb import __version__
from stb.cli.config import config
from stb.cli.press import press


@click.group()
@click.version_option(version=__version__, prog_name="stb")
def stb():
    """stb cli tool to help create tests"""


stb.add_command(press)
stb.add_command(config)
