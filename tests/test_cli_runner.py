from stb import __version__
from stb.cli.runner import stb


def test_that_help_menu_shows_with_cli_name(runner):
    result = runner.invoke(stb)
    assert result.exit_code == 0
    assert "stb cli tool to help create tests" in result.output


def test_that_version_outputs_correctly(runner):
    result = runner.invoke(stb, ["--version"])
    assert result.exit_code == 0
    assert result.output == f"stb, version {__version__}\n"
