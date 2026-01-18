import yaml
import glob
import os
from pathlib import Path

ASSETS_DIR = Path(__file__).parent


def load_assets(asset_type: str = None) -> list:
    """
    Load tickers from YAML files in the assets directory.

    Args:
        asset_type (str, optional): The subdirectory to search (e.g., 'Stocks', 'ETFs').
                                    If None, searches all subdirectories.

    Returns:
        list: A unique list of tickers found.
    """
    tickers = set()

    search_pattern = f"{asset_type}/*.yml" if asset_type else "**/*.yml"
    files = list(ASSETS_DIR.glob(search_pattern))

    for file_path in files:
        with open(file_path, "r") as f:
            try:
                data = yaml.safe_load(f)
                if data and "tickers" in data:
                    tickers.update(data["tickers"])
            except yaml.YAMLError as exc:
                print(f"Error reading {file_path}: {exc}")

    return list(tickers)


def discover_assets() -> dict:
    """
    Discover all assets organized by category.

    Returns:
        dict: Keys are categories (subfolders), values are lists of tickers.
    """
    assets = {}
    for item in ASSETS_DIR.iterdir():
        if item.is_dir() and item.name != "__pycache__":
            assets[item.name] = load_assets(item.name)

    return assets


if __name__ == "__main__":
    # Test
    all_assets = discover_assets()
    for category, tickers in all_assets.items():
        print(f"{category}: {len(tickers)} tickers found.")
        print(tickers[:5])
