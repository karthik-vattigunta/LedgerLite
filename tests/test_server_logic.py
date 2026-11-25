import unittest
from decimal import Decimal

from ledgerlite.enums import AccountType, Currency, Direction, KYCStatus
from ledgerlite.models import Account, Customer, LedgerEntry
from ledgerlite.money import Money
from ledgerlite.web.server import account_to_dict, seed_accounts


def make_account(balance: str | None = None) -> Account:
    owner = Customer("C1", "Ramya", KYCStatus.VERIFIED)
    account = Account("A9", owner, AccountType.SAVINGS, Currency.EUR)
    if balance is not None:
        money = Money(Decimal(balance), Currency.EUR)
        account.post(LedgerEntry("A9", money, Direction.CREDIT))
    return account


class TestSeedAccounts(unittest.TestCase):

    def test_a1_and_a2_exist(self):
        self.assertEqual(set(seed_accounts()), {"A1", "A2"})

    def test_a1_starts_with_500(self):
        self.assertEqual(seed_accounts()["A1"].balance(), Decimal("500.00"))

    def test_a2_starts_empty(self):
        self.assertEqual(seed_accounts()["A2"].balance(), Decimal("0"))

    def test_each_call_gives_fresh_accounts(self):
        first = seed_accounts()
        second = seed_accounts()
        self.assertIsNot(first["A1"], second["A1"])


class TestAccountToDict(unittest.TestCase):

    def test_fields(self):
        result = account_to_dict(make_account("25.50"))
        self.assertEqual(result["id"], "A9")
        self.assertEqual(result["type"], "SAVINGS")
        self.assertEqual(result["currency"], "EUR")

    def test_balance_is_a_string(self):
        result = account_to_dict(make_account("25.50"))
        self.assertEqual(result["balance"], "25.50")
        self.assertIsInstance(result["balance"], str)

    def test_empty_account_balance_is_a_string(self):
        self.assertEqual(account_to_dict(make_account())["balance"], "0")

    def test_decimal_precision_is_kept(self):
        result = account_to_dict(make_account("0.30"))
        self.assertEqual(result["balance"], "0.30")


if __name__ == "__main__":
    unittest.main()