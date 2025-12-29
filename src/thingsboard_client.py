import time
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple

import requests


@dataclass(frozen=True)
class ThingsBoardConfig:
    host: str = "https://thingsboard.cloud"
    device_token: str = "4lzxxn96epsem7gn3wiz"
    timeout_s: int = 10
    retries: int = 3
    backoff_s: float = 1.0


class ThingsBoardClient:
    """
    Telemetry upload client using HTTP POST + JSON.
    """
    def __init__(self, cfg: ThingsBoardConfig):
        self.cfg = cfg

    @property
    def telemetry_url(self) -> str:
        return f"{self.cfg.host.rstrip('/')}/api/v1/{self.cfg.device_token}/telemetry"

    def send_telemetry(self, payload: Dict[str, Any]) -> Tuple[bool, Optional[int], str]:
        """
        Sends telemetry with basic retry/backoff.
        Returns: (ok, http_status, message)
        """
        last_status = None
        last_err = ""

        for attempt in range(1, self.cfg.retries + 1):
            try:
                r = requests.post(self.telemetry_url, json=payload, timeout=self.cfg.timeout_s)
                last_status = r.status_code
                if r.status_code == 200:
                    return True, r.status_code, "OK"
                last_err = f"HTTP {r.status_code}: {r.text[:200]}"
            except requests.RequestException as e:
                last_err = f"Request error: {e}"

            time.sleep(self.cfg.backoff_s * attempt)

        return False, last_status, last_err
