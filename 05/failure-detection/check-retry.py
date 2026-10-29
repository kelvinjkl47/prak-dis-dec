"""
Retry dengan tenacity.

Mencoba mengakses aplikasi Blacksheep berulang kali. Jika masih gagal setelah
batas percobaan, tenacity melempar RetryError.

Pemakaian:
    python check-retry.py
"""

import requests
from tenacity import RetryError, retry, stop_after_attempt, wait_fixed

URL = "http://localhost:44777"


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def access_server() -> str:
    print(f"Attempting to access {URL}...")
    response = requests.get(URL, timeout=3)
    response.raise_for_status()
    return response.text


def main() -> None:
    try:
        access_server()
    except RetryError as error:
        print(f"Failed to access URL after multiple retries: {error}")
    else:
        print(f"Successfully accessed {URL}")


if __name__ == "__main__":
    main()
