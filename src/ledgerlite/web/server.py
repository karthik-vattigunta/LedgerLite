"""A tiny LedgerLite HTTP server.

Run it from the project root:
    uv run python -m ledgerlite.web.server
"""

import json
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

from ..enums import AccountType, Currency, Direction, KYCStatus
from ..models import Account, Customer, LedgerEntry
from ..money import Money

HOST = "127.0.0.1"
PORT = 8000


def seed_accounts() -> dict[str, Account]:
    owner = Customer("C1", "Ramya", KYCStatus.VERIFIED)
    a1 = Account("A1", owner, AccountType.CHECKING, Currency.USD)
    a2 = Account("A2", owner, AccountType.SAVINGS, Currency.USD)
    opening = Money(Decimal("500.00"), Currency.USD)
    a1.post(LedgerEntry("A1", opening, Direction.CREDIT))
    return {"A1": a1, "A2": a2}


ACCOUNTS = seed_accounts()


def account_to_dict(account: Account) -> dict:
    return {
        "id": account.account_id,
        "type": account.account_type.value,
        "currency": account.currency.value,
        "balance": str(account.balance()),
    }


class Handler(BaseHTTPRequestHandler):
    """Answers one request."""

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        parts = path.strip("/").split("/")

        if path == "/health":
            self.send_json(200, {"status": "ok"})
        elif len(parts) == 2 and parts[0] == "accounts":
            account = ACCOUNTS.get(parts[1])
            if account is None:
                self.send_json(404, {"title": "Account not found", "status": 404,
                                     "detail": f"No account {parts[1]}"})
            else:
                self.send_json(200, account_to_dict(account))
        else:
            self.send_json(404, {"title": "Not found", "status": 404,
                                 "detail": f"Nothing at {path}"})


def main() -> None:
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Listening on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()