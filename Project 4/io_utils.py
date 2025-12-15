import csv
import json
from pathlib import Path
from library import Book

def import_books_csv(catalog, path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            book = Book(
                row["title"],
                row["isbn"],
                int(row["year"]),
                row["author"],
                row["genre"]
            )
            catalog.add_item(book)

def export_report(loan_manager, path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(loan_manager.checkouts, f, indent=2)
 
