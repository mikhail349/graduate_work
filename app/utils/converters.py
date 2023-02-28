def money_to_float(value: int) -> float:
    """Конвертировать копейки в рубли.

    Args:
        value: цена в копейках

    Returns:
        float: цена в рублях

    """
    return value / 100


def money_to_int(value: float) -> int:
    """Конвертировать рубли в копейки.

    Args:
        value: цена в рублях

    Returns:
        int: цена в копейках

    """
    return int(value * 100)
