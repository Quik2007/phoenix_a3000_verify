from decimal import Decimal, getcontext
import re

getcontext().prec = 12


def get_decimal(text: str) -> Decimal:
    if not re.fullmatch("(0|[1-9]\d*),\d{2}", text) or not isinstance(text, str):
        raise ValueError(f"Ungültiger Preis: {text}")
    return Decimal(text.replace(",", "."))


class FormatChange(FutureWarning):
    def __init__(self, msg: str):
        super().__init__(msg)

class UserError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


Aufträge = dict[str, Decimal]
