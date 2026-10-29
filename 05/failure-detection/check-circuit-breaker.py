"""
Circuit breaker sederhana (closed -> open -> half-open -> closed).

- closed    : request diizinkan dan kegagalan dihitung.
- open      : request langsung ditolak tanpa memanggil server (fail fast)
              sampai recovery timeout habis.
- half-open : sejumlah request percobaan diizinkan; jika berhasil kembali
              ke closed, jika gagal kembali ke open.

Pemakaian:
    python check-circuit-breaker.py
"""

import time

import requests

URL = "http://localhost:44777"

FAILURE_THRESHOLD = 3   # jumlah kegagalan sebelum circuit dibuka
RECOVERY_TIMEOUT = 5.0  # detik sebelum mencoba lagi (half-open)
HALF_OPEN_MAX_CALLS = 1 # request percobaan yang diizinkan saat half-open
MAX_ATTEMPTS = 10       # jumlah percobaan pada script demo


class CircuitBreakerOpenError(Exception):
    """Dilempar ketika circuit breaker menolak request (status open)."""


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = FAILURE_THRESHOLD,
        recovery_timeout: float = RECOVERY_TIMEOUT,
        half_open_max_calls: int = HALF_OPEN_MAX_CALLS,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.state = "closed"
        self.failure_count = 0
        self.opened_at: float | None = None
        self.half_open_calls = 0

    def call(self, func):
        self._check_recovery()

        if self.state == "open":
            raise CircuitBreakerOpenError("Circuit is open - request blocked")

        if self.state == "half-open":
            if self.half_open_calls >= self.half_open_max_calls:
                raise CircuitBreakerOpenError(
                    "Circuit is half-open - trial request already in progress"
                )
            self.half_open_calls += 1

        try:
            result = func()
        except requests.RequestException:
            self._on_failure()
            raise
        else:
            self._on_success()
            return result

    def _check_recovery(self) -> None:
        if (
            self.state == "open"
            and self.opened_at is not None
            and time.monotonic() - self.opened_at >= self.recovery_timeout
        ):
            self.state = "half-open"
            self.half_open_calls = 0
            print("[circuit-breaker] open -> half-open (mencoba pulih)")

    def _on_failure(self) -> None:
        self.failure_count += 1

        if self.state == "half-open" or self.failure_count >= self.failure_threshold:
            self.state = "open"
            self.opened_at = time.monotonic()
            self.half_open_calls = 0
            print(
                f"[circuit-breaker] -> open setelah {self.failure_count} kegagalan, "
                f"request berikutnya ditolak selama {self.recovery_timeout} detik"
            )

    def _on_success(self) -> None:
        if self.state != "closed":
            print(f"[circuit-breaker] {self.state} -> closed (layanan pulih)")

        self.state = "closed"
        self.failure_count = 0
        self.opened_at = None
        self.half_open_calls = 0


def request_server() -> requests.Response:
    response = requests.get(URL, timeout=3)
    response.raise_for_status()
    return response


def main() -> None:
    breaker = CircuitBreaker()

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"Attempting to access {URL}...")
        try:
            breaker.call(request_server)
        except CircuitBreakerOpenError as error:
            print(f"Ditolak circuit breaker: {error}")
        except requests.RequestException as error:
            print(f"Gagal mengakses server: {type(error).__name__}")
        else:
            print(f"Successfully accessed {URL}")

        time.sleep(1)


if __name__ == "__main__":
    main()
