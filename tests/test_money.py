import unittest
from dataclasses import FrozenInstanceError
from decimal import Decimal

from ledgerlite.enums import Currency
from ledgerlite.errors import InvalidAmountError, LedgeError
from ledgerlite.money import Money

class TestFloatVsDecimal(unittest.TestCase):

    def test_float_addition_is_inexact(self):
        self.assertNotEqual(0.1 + 0.2, 0.3)

    def test_decimal_addition_is_exact(self):
        self.assertEqual(Decimal("0.1") + Decimal("0.2"), Decimal("0.3"))

    def test_decimal_from_float_keeps_the_error(self):
        self.assertNotEqual(Decimal(0.1), Decimal("0.1"))

class TestMoney(unittest.TestCase):

    def test_valid_money_is_created(self):
        m=Money(Decimal("10.50"), Currency.USD)
        self.assertEqual(m.amount, Decimal("10.50"))
        self.assertEqual(m.currency, Currency.USD)

    def test_zero_amount_is_rejected(self):
        with self.assertRaises(InvalidAmountError):
            Money(Decimal("-5"), Currency.USD)

    def test_negative_amount_is_rejected(self):
        with self.assertRaises(InvalidAmountError):
            Money(Decimal("-5"), Currency.USD)

    def test_invalid_amount_is_a_ledger_error(self):
        with self.assertRaises(LedgeError):
            Money(Decimal("-1"), Currency.USD)

    def test_money_is_immutable(self):
        m = Money(Decimal("10"), Currency.USD)
        with self.assertRaises(FrozenInstanceError):
            m.amount = Decimal("999")

    def test_equal_money_compares_equal(self):
        self.assertEqual(
            Money(Decimal("5"), Currency.EUR),
            Money(Decimal("5"), Currency.EUR),
        )

if __name__ == "__main__":
    unittest.main()


