"""Call the LedgerLite server with httpx and print what comes back.

Start the server in one terminal:
    uv run python -m ledgerlite.web.server
Then run this in a second terminal:
    uv run python -m ledgerlite.web.client
"""

import httpx

BASE_URL = "http://127.0.0.1:8000"

def show(title:str, response: httpx.Response) -> None:
    """ Print the request, the status and  the main headers """
    print(f"\n=={title}")
    print(f"{response.request.method} {response.request.url.path} "
          f"{response.status_code} {response.reason_phrase}")
    for name in ("content-type", "content-length"):
        if name in response.headers:
            print(f"{name}: {response.headers[name]}")
    print(f"  body:{response.text}")

def main() -> None:
    with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
        show("Health check", client.get("/health"))
        show("Account A1", client.get("/accounts/A1"))
        show("Account A2", client.get("/accounts/A2"))
        show("Unknown account (404)", client.get("/accounts/NOPE"))
        show("Unknown path (404)", client.get("/whatever"))
        show("Query string is ignored", client.get("/accounts/A1?x=1"))
        show("POST not supported yet (501)", client.post("/accounts/A1"))

if __name__ == "__main__":
    try:
        main()
    except httpx.ConnectError:
        print(f"Could not connect to {BASE_URL}. Start the server first.")