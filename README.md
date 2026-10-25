# Лабораторная 1. Консольный набор утилит

Калькулятор и конвертер величин.

## Структура проекта

```text
lab_01/
  pyproject.toml
  README.md
  src/toolkit/
    __init__.py
    __main__.py     # CLI
    calculator.py   # калькулятор
    converter.py    # конвертер
    errors.py       # классы ошибок
  tests/
    test_calculator.py
    test_converter.py
    test_cli.py
```

## Функции

calculator.py
- tokenize — разбивает строку на токены
- validate — проверяет порядок токенов, отмечает унарные знаки
- to_rpn — переводит выражение в обратную польскую запись
- eval_rpn — вычисляет RPN стеком
- calculate — вычисляет выражение целиком

converter.py
- convert — переводит значение между единицами

__main__.py
- build_parser — аргументы командной строки
- main — запускает команду, возвращает код выхода (0 или 2)

## Как запустить

Из папки lab_01. macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest ruff
export PYTHONPATH=src
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install pytest ruff
$env:PYTHONPATH = "src"
```

## Команды CLI

Справка:

```bash
python -m toolkit --help
python -m toolkit calc --help
python -m toolkit convert --help
```

Калькулятор:

```bash
python -m toolkit calc "2+3*4"            # 14
python -m toolkit calc "10 / 4"           # 2.5
python -m toolkit calc "(2+3)*4"          # 20
python -m toolkit calc "1,5+1.5"          # 3
python -m toolkit calc "7//2"             # 3
python -m toolkit calc "7%3"              # 1
python -m toolkit calc "1+-2"             # -1
python -m toolkit calc -- "-2*-3"         # 6
python -m toolkit calc -- "-7//2"         # -4
python -m toolkit calc -- "-7%3"          # 2
```

Если выражение начинается с минуса, перед ним ставится --.

Конвертер (регистр единиц не важен):

```bash
python -m toolkit convert 1000 --from mm --to m      # 1
python -m toolkit convert 1.5 --from kg --to g       # 1500
python -m toolkit convert 1,5 --from KM --to M       # 1500
python -m toolkit convert 0 --from c --to f          # 32
python -m toolkit convert 212 --from f --to c        # 100
python -m toolkit convert -273.15 --from c --to k    # 0
```

Ошибки (сообщение в stderr, код возврата 2):

```bash
python -m toolkit calc ""                            # пустое выражение
python -m toolkit calc "2*/3"                        # два оператора подряд
python -m toolkit calc "2+a"                         # недопустимый символ
python -m toolkit calc "1/0"                         # деление на ноль
python -m toolkit convert 1 --from kg --to m         # несовместимые единицы
python -m toolkit convert 1 --from mile --to m       # неизвестная единица
python -m toolkit convert -300 --from c --to k       # ниже абсолютного нуля
python -m toolkit convert abc --from m --to km       # неверное число
echo $?                                              # код возврата последней команды
```

## Тесты и проверка кода

```bash
python -m pytest
ruff check .
```
