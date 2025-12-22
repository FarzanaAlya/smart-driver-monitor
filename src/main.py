import os
from dotenv import load_dotenv

from src.thingsboard_client import ThingsBoardConfig
from src.runner import run_pipeline

def main() -> None:
    load_dotenv()  # loads .env from project root

    tb_host = os.getenv("TB_HOST", "").strip()
    tb_token = os.getenv("TB_TOKEN", "").strip()

    if not tb_host or not tb_token:
        raise RuntimeError(
            "Missing TB_HOST/TB_TOKEN. Create a .env file in the project root with:\n"
            "TB_HOST=https://thingsboard.cloud\n"
            "TB_TOKEN=<your device token>"
        )

    tb_cfg = ThingsBoardConfig(host=tb_host, device_token=tb_token)

    # Run continuously (stop with Ctrl+C)
    run_pipeline(tb_cfg, max_samples=None)

if __name__ == "__main__":
    main()
