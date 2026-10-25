import subprocess
import sys

from toolkit.__main__ import main


def test_cli_calc(capsys):
    assert main(["calc", "2+3*4"]) == 0
    assert capsys.readouterr().out.strip() == "14"


def test_cli_negative_expr(capsys):
    assert main(["calc", "--", "-2*-3"]) == 0
    assert capsys.readouterr().out.strip() == "6"


def test_cli_error_stderr(capsys):
    assert main(["calc", "1/0"]) == 2
    cap = capsys.readouterr()
    assert cap.out == "" and "деление на ноль" in cap.err


def test_cli_convert(capsys):
    assert main(["convert", "0", "--from", "c", "--to", "f"]) == 0
    assert capsys.readouterr().out.strip() == "32"


def test_help_subprocess():
    r = subprocess.run([sys.executable, "-m", "toolkit", "--help"], capture_output=True, check=False,
                       env={"PYTHONPATH": "src"})
    assert r.returncode == 0
