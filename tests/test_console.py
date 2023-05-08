import pytest
import typer.testing
from typer.testing import CliRunner

from krtools.__main__ import app


@pytest.fixture
def runner() -> CliRunner:
    return typer.testing.CliRunner()


def test_main_version_succeeds(runner: CliRunner) -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0, "The program should exit gracefully."


def test_main_help_succeeds(runner: CliRunner) -> None:
    result = runner.invoke(app, ["--help"])
    assert "KR Tools" in result.output, "The correct help message should be displayed."
    assert result.exit_code == 0, "The program should exit gracefully."
