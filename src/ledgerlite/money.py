"""Money: an amount and a currency, always valid."""

from dataclasses import dataclass
from decimal import Decimal

from .enums import Currency
from .errors import InvalidAmountError

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: Currency

    def __post_init__(self):
        if self.amount <= 0:
            raise InvalidAmountError(self.amount)

