"""Domain models: customers, accounts, ledger entries and transfers."""

from dataclasses import dataclass, field
from decimal import Decimal

from .enums import AccountType, Currency, Direction, KYCStatus
from .errors import CurrencyMissmatchError, SameAccountTransferError
from .money import Money


@dataclass(frozen=True)
class Customer:
    customer_id: str
    name: str
    kyc_status: KYCStatus = KYCStatus.PENDING


@dataclass(frozen=True)
class LedgerEntry:
    account_id: str
    money: Money
    direction: Direction


@dataclass
class Account:
    account_id: str
    owner: Customer
    account_type: AccountType
    currency: Currency
    entries: list[LedgerEntry] = field(default_factory=list)

    def post(self, entry: LedgerEntry) -> None:
        """Add an entry to this account's history."""
        if entry.money.currency != self.currency:
            raise CurrencyMissmatchError(self.currency, entry.money.currency)
        self.entries.append(entry)

    def balance(self) -> Decimal:
        """Credits minus debits."""
        total = Decimal("0")
        for entry in self.entries:
            if entry.direction == Direction.CREDIT:
                total += entry.money.amount
            else:
                total -= entry.money.amount
        return total


@dataclass(frozen=True)
class Transfer:
    source: Account
    destination: Account
    money: Money

    def __post_init__(self):
        if self.source.account_id == self.destination.account_id:
            raise SameAccountTransferError(self.source.account_id)
        # Check both sides up front, so a transfer never half-happens.
        for account in (self.source, self.destination):
            if self.money.currency != account.currency:
                raise CurrencyMissmatchError(account.currency, self.money.currency)

    def execute(self) -> None:
        """Record the transfer as two matching entries (double-entry)."""
        self.source.post(
            LedgerEntry(self.source.account_id, self.money, Direction.DEBIT)
        )
        self.destination.post(
            LedgerEntry(self.destination.account_id, self.money, Direction.CREDIT)
        )