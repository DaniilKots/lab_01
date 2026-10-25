import math

from .errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    InvalidNumberError,
    UnknownUnitError,
)

LENGTH = (("mm", 0.001), ("cm", 0.01), ("m", 1.0), ("km", 1000.0))
MASS = (("g", 1.0), ("kg", 1000.0))
TEMPERATURE = ("c", "f", "k")
EPS = 1e-9  # допуск для сравнения с абсолютным нулём


def _factor(table: tuple[tuple[str, float], ...], unit: str) -> float | None:
    """Возвращает коэффициент единицы или None, если её нет в таблице."""
    for name, factor in table:
        if name == unit:
            return factor
    return None


def _group(unit: str) -> str:
    """Возвращает группу единицы."""
    if _factor(LENGTH, unit) is not None:
        return "length"
    if _factor(MASS, unit) is not None:
        return "mass"
    if unit in TEMPERATURE:
        return "temperature"
    raise UnknownUnitError(f"неизвестная единица: {unit!r}")


def _to_kelvin(x: float, unit: str) -> float:
    if unit == "c":
        return x + 273.15
    if unit == "f":
        return (x - 32) * 5 / 9 + 273.15
    return x


def _from_kelvin(k: float, unit: str) -> float:
    if unit == "c":
        return k - 273.15
    if unit == "f":
        return (k - 273.15) * 9 / 5 + 32
    return k


def convert(value: float | str, src: str, dst: str) -> float:
    """Переводит значение из одной единицы в другую внутри одной группы."""
    try:
        x = float(str(value).replace(",", "."))  # запятая как точка
    except (TypeError, ValueError):
        raise InvalidNumberError(f"неверное числовое значение: {value!r}") from None
    if not math.isfinite(x):
        raise InvalidNumberError(f"неверное числовое значение: {value!r}")
    src, dst = src.lower(), dst.lower()
    group = _group(src)
    if group != _group(dst):
        raise IncompatibleUnitsError(f"несовместимые единицы: {src} и {dst}")
    if group == "length":
        return x * _factor(LENGTH, src) / _factor(LENGTH, dst)
    if group == "mass":
        return x * _factor(MASS, src) / _factor(MASS, dst)
    kelvin = _to_kelvin(x, src)
    if kelvin < -EPS:
        raise BelowAbsoluteZeroError("температура ниже абсолютного нуля")
    return _from_kelvin(max(kelvin, 0.0), dst)
