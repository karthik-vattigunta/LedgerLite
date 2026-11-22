"""Fixed sets of allowed values used across the bank domain."""

from enum import Enum

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    INR = "INR"
    GBP = "GBP"

class KYCStatus(Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"

class AccountType(Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"

class Direction(Enum):
    DEBIT = "debit"
    CREDIT = "credit"