import json
from pathlib import Path
from library import Book, DVD, EBook

def save_catalog(catalog, path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump([item.to_dict() for item in catalog.all_items()], f, indent=2)

def load_catalog(catalog, path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return

    catalog.items.clear()

    for record in data:
        item_type = record.pop("type")
        if item_type == "Book":
            item = Book(**record)
        elif item_type == "DVD":
            item = DVD(**record)
        elif item_type == "EBook":
            item = EBook(**record)
        else:
            continue
        catalog.add_item(item)

def save_checkouts(loan_manager, path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(loan_manager.checkouts, f, indent=2)

def load_checkouts(loan_manager, path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            loan_manager.checkouts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        loan_manager.checkouts = {}
