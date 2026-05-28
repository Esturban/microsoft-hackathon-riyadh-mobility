from __future__ import annotations

import json
from pathlib import Path

import httpx


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

DATASETS = {
    "metro": "https://opendata.rcrc.gov.sa/api/explore/v2.1/catalog/datasets/metro-lines-in-riyadh-2024/records?limit=100",
    "bus": "https://opendata.rcrc.gov.sa/api/explore/v2.1/catalog/datasets/bus-roads-by-direction-in-riyadh-2024/records?limit=100",
}


def fetch_dataset(name: str, url: str) -> None:
    output = RAW_DIR / f"{name}.json"
    try:
        response = httpx.get(url, timeout=30.0)
        response.raise_for_status()
        output.write_text(json.dumps(response.json(), indent=2), encoding="utf-8")
        print(f"saved {name} -> {output}")
    except Exception as exc:
        print(f"failed {name}: {exc}")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, url in DATASETS.items():
        fetch_dataset(name, url)


if __name__ == "__main__":
    main()
