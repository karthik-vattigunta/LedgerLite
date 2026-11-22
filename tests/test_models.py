import unittest
from decimal import Decimal

from ledgerlite.enums import AccountType, Currency, Direction, KYCStatus
from ledgerlite.errors import CurrencyMissmatchError, SameAccountTransferError
from ledgerlite.models import Account, Customer, LedgerEntry, Transfer
from ledgerlite.money import Money


def make_account(account_id: str, currency: Currency = Currency.USD) -> Account:
    """Helper so each test doesn't repeat the setup."""
    owner = Customer("C1", "deft", KYCStatus.VERIFIED)
    return Account(account_id, owner, AccountType.CHECKING, currency)


def usd(amount: str) -> Money:
    return Money(Decimal(amount), Currency.USD)


class TestCustomer(unittest.TestCase):

    def test_kyc_defaults_to_pending(self):
        customer = Customer("C1", "deft")
        self.assertEqual(customer.kyc_status, KYCStatus.PENDING)

    def test_kyc_can_be_set(self):
        customer = Customer("C1", "deft", KYCStatus.VERIFIED)
        self.assertEqual(customer.kyc_status, KYCStatus.VERIFIED)


class TestAccount(unittest.TestCase):

    def test_new_account_has_zero_balance(self):
        self.assertEqual(make_account("A1").balance(), Decimal("0"))

    def test_each_account_gets_its_own_entries_list(self):
        a = make_account("A1")
        b = make_account("A2")
        a.post(LedgerEntry("A1", usd("10"), Direction.CREDIT))
        self.assertEqual(len(b.entries), 0)

    def test_credit_increases_and_debit_decreases_balance(self):
        account = make_account("A1")
        account.post(LedgerEntry("A1", usd("100"), Direction.CREDIT))
        account.post(LedgerEntry("A1", usd("30"), Direction.DEBIT))
        self.assertEqual(account.balance(), Decimal("70"))

    def test_posting_wrong_currency_is_rejected(self):
        account = make_account("A1", Currency.USD)
        euros = Money(Decimal("10"), Currency.EUR)
        with self.assertRaises(CurrencyMissmatchError):
            account.post(LedgerEntry("A1", euros, Direction.CREDIT))

    def test_savings_account_type(self):
        owner = Customer("C1", "deft")
        account = Account("S1", owner, AccountType.SAVINGS, Currency.USD)
        self.assertEqual(account.account_type, AccountType.SAVINGS)


class TestTransfer(unittest.TestCase):

    def test_transfer_moves_money(self):
        src = make_account("A1")
        dst = make_account("A2")
        src.post(LedgerEntry("A1", usd("100"), Direction.CREDIT))

        Transfer(src, dst, usd("40")).execute()

        self.assertEqual(src.balance(), Decimal("60"))
        self.assertEqual(dst.balance(), Decimal("40"))

    def test_transfer_creates_two_entries(self):
        src = make_account("A1")
        dst = make_account("A2")
        Transfer(src, dst, usd("40")).execute()
        self.assertEqual(src.entries[-1].direction, Direction.DEBIT)
        self.assertEqual(dst.entries[-1].direction, Direction.CREDIT)

    def test_transfer_to_same_account_is_rejected(self):
        account = make_account("A1")
        with self.assertRaises(SameAccountTransferError):
            Transfer(account, account, usd("10"))

    def test_transfer_currency_must_match_source(self):
        src = make_account("A1", Currency.EUR)
        dst = make_account("A2", Currency.USD)
        with self.assertRaises(CurrencyMissmatchError):
            Transfer(src, dst, usd("10"))

    def test_transfer_currency_must_match_destination(self):
        src = make_account("A1", Currency.USD)
        dst = make_account("A2", Currency.EUR)
        with self.assertRaises(CurrencyMissmatchError):
            Transfer(src, dst, usd("10"))

    def test_failed_transfer_leaves_no_entries(self):
        src = make_account("A1", Currency.USD)
        dst = make_account("A2", Currency.EUR)
        with self.assertRaises(CurrencyMissmatchError):
            Transfer(src, dst, usd("10")).execute()
        self.assertEqual(src.entries, [])


if __name__ == "__main__":
    unittest.main()
