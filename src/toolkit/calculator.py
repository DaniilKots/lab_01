from .errors import (
    ConsecutiveOperatorsError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    InvalidNumberError,
    MissingOperandError,
    ParenthesesError,
)

BINARY = {"+": 1, "-": 1, "*": 2, "/": 2, "//": 2, "%": 2}
UNARY = {"u+": 3, "u-": 3}  # выше приоритет, чем у бинарных


def tokenize(expr: str) -> list[str]:
    """Разбивает строку на числа, операторы и скобки."""
    tokens: list[str] = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit() or ch in ".,":
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] in ".,"):
                j += 1
            num = expr[i:j].replace(",", ".")  # запятая как точка
            if num.count(".") > 1 or num == ".":
                raise InvalidNumberError(f"неверное число: {num!r}")
            tokens.append(num)
            i = j
        elif expr.startswith("//", i):
            tokens.append("//")
            i += 2
        elif ch in "+-*/%()":
            tokens.append(ch)
            i += 1
        else:
            raise InvalidCharacterError(f"недопустимый символ: {ch!r}")
    return tokens


def validate(tokens: list[str]) -> list[str]:
    """Проверяет порядок токенов и помечает унарные знаки."""
    if not tokens:
        raise EmptyExpressionError("пустое выражение")
    result: list[str] = []
    want_operand = True
    depth = 0
    for tok in tokens:
        if tok == "(":
            if not want_operand:
                raise MissingOperandError("пропущен оператор перед '('")
            depth += 1
        elif tok == ")":
            if want_operand:
                raise MissingOperandError("пропущен операнд перед ')'")
            depth -= 1
            if depth < 0:
                raise ParenthesesError("лишняя ')'")
        elif tok in BINARY:
            if want_operand:
                if tok not in ("+", "-"):
                    raise ConsecutiveOperatorsError(f"два оператора подряд или нет операнда: {tok!r}")
                tok = "u" + tok
            else:
                want_operand = True
        else:  # число
            if not want_operand:
                raise MissingOperandError("пропущен оператор между числами")
            want_operand = False
        result.append(tok)
    if want_operand:
        raise MissingOperandError("пропущен операнд в конце выражения")
    if depth:
        raise ParenthesesError("не закрыта '('")
    return result


def to_rpn(tokens: list[str]) -> list[str]:
    """Переводит инфиксную запись в обратную польскую."""
    out: list[str] = []
    ops: list[str] = []
    prec = {**BINARY, **UNARY}
    for tok in tokens:
        if tok == "(":
            ops.append(tok)
        elif tok == ")":
            while ops[-1] != "(":
                out.append(ops.pop())
            ops.pop()
        elif tok in prec:
            while ops and ops[-1] != "(" and (
                prec[ops[-1]] > prec[tok] or (prec[ops[-1]] == prec[tok] and tok not in UNARY)
            ):
                out.append(ops.pop())
            ops.append(tok)
        else:
            out.append(tok)
    while ops:
        out.append(ops.pop())
    return out


def eval_rpn(rpn: list[str]) -> float:
    """Вычисляет выражение в RPN с помощью стека."""
    stack: list[float] = []
    for tok in rpn:
        if tok in UNARY:
            x = stack.pop()
            stack.append(-x if tok == "u-" else x)
        elif tok in BINARY:
            b, a = stack.pop(), stack.pop()
            if tok == "+":
                stack.append(a + b)
            elif tok == "-":
                stack.append(a - b)
            elif tok == "*":
                stack.append(a * b)
            else:
                if b == 0:
                    raise DivisionByZeroError("деление на ноль")
                if tok == "/":
                    stack.append(a / b)
                elif tok == "//":
                    stack.append(a // b)  # округление вниз
                else:
                    stack.append(a % b)  # знак как у делителя
        else:
            stack.append(float(tok))
    return stack[0]


def calculate(expr: str) -> float:
    """Вычисляет выражение."""
    return eval_rpn(to_rpn(validate(tokenize(expr))))
