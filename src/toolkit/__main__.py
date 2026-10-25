import argparse
import sys

from .calculator import calculate
from .converter import convert
from .errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов командной строки."""
    p = argparse.ArgumentParser(prog="toolkit", description="Калькулятор и конвертер величин")
    sub = p.add_subparsers(dest="command", required=True)
    c = sub.add_parser("calc", help="вычислить выражение")
    c.add_argument("expression")
    v = sub.add_parser("convert", help="конвертировать величину")
    v.add_argument("value")
    v.add_argument("--from", dest="src", required=True, metavar="UNIT")
    v.add_argument("--to", dest="dst", required=True, metavar="UNIT")
    return p


def main(argv: list[str] | None = None) -> int:
    """Запускает команду и возвращает код выхода: 0 при успехе, 2 при ошибке."""
    args = build_parser().parse_args(argv)
    try:
        if args.command == "calc":
            result = calculate(args.expression)
        else:
            result = convert(args.value, args.src, args.dst)
    except ToolkitError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 2
    print(f"{result:.12g}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
