class ToolkitError(ValueError):
    """Базовая пользовательская ошибка."""


class EmptyExpressionError(ToolkitError):
    """Пустое выражение."""


class InvalidCharacterError(ToolkitError):
    """Недопустимый символ."""


class InvalidNumberError(ToolkitError):
    """Неверное числовое значение."""


class MissingOperandError(ToolkitError):
    """Пропущенный операнд или оператор."""


class ConsecutiveOperatorsError(ToolkitError):
    """Два бинарных оператора подряд."""


class ParenthesesError(ToolkitError):
    """Несбалансированные скобки."""


class DivisionByZeroError(ToolkitError):
    """Деление на ноль."""


class UnknownUnitError(ToolkitError):
    """Неизвестная единица."""


class IncompatibleUnitsError(ToolkitError):
    """Единицы из разных групп."""


class BelowAbsoluteZeroError(ToolkitError):
    """Температура ниже абсолютного нуля."""
