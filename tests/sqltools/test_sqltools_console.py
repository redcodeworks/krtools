import pytest
import typer.testing
from typer.testing import CliRunner

from krtools.__main__ import app


@pytest.fixture
def runner() -> CliRunner:
    return typer.testing.CliRunner()


def test_main_help_succeeds(runner: CliRunner) -> None:
    result = runner.invoke(app, ["sql", "--help"])
    assert "SQL" in result.output, "There should be the correct help message."
    assert result.exit_code == 0, "The program should exit gracefully."
