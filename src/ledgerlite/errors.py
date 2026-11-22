""" Domain errors: each class names the bussiness rule that was broken."""

from decimal import Decimal
from .enums import Currency

class LedgeError(Exception):
    """ Base class for every rule the ledger refuses to break."""

class InvalidAmountError(LedgeError):
    """ An amount was zero or negative."""

    def __init__(self, amount: Decimal):
        self.amount = amount
        super().__init__(f"Amount must be greater than zero, got {amount}")

class CurrencyMissmatchError(LedgeError):
    """ Money was in one currency was used where need to use other currency was required.."""

    def __init__(self, expected:Currency, got:Currency):
        self.expected = expected
        self.got = got
        super().__init__(
            f"Currency mismatch: expected {expected.value}, got {got.value}"
        )

class SameAccountTransferError(LedgeError):
    """ A transfer was being happening in the same account. """

    def __init__(self, account_id:str):
        self.account_id = account_id
        super().__init__(f"Cannot transfer from account {account_id} to itself.")