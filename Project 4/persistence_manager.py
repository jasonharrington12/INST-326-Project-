from library_model import LibraryCatalog, LoanManager, ITEM_CLASS_MAP
from library_model import Book, DVD, EBook, LibraryItem
from pathlib import Path
import json
import csv
from typing import Dict, Any, Tuple, List
from datetime import date

# Define file paths using pathlib
DATA_DIR = Path("./data")
STATE_FILE = DATA_DIR / "library_state.json"
REPORT_FILE = DATA_DIR / "loan_report.txt"

class PersistenceManager:
    
    def __init__(self, catalog: LibraryCatalog, loan_manager: LoanManager):
        self._catalog = catalog
        self._loan_manager = loan_manager
        
        if not DATA_DIR.exists():
            DATA_DIR.mkdir()

    def save_state(self) -> str:
        print(f"Attempting to save state to {STATE_FILE}...")
        try:
            state = {
                "catalog_items": [item.to_dict() for item in self._catalog.all_items],
                "checkouts": self._loan_manager.checkouts_to_dict()
            }
            
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)
            
            return f"System state successfully saved to {STATE_FILE}"
        
        except IOError as e:
            return f"ERROR: Failed to save state due to file operation error: {e}"
        except Exception as e:
            return f"ERROR: An unexpected error occurred during save: {e}"


    def load_state(self) -> str:
        if not STATE_FILE.exists():
            return f"INFO: State file not found at {STATE_FILE}. Starting with an empty state."

        print(f"Attempting to load state from {STATE_FILE}...")
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)

            loaded_count = 0
            self._catalog._items.clear() 
            
            for item_data in state.get("catalog_items", []):
                item_type = item_data.get("type")
                if item_type in ITEM_CLASS_MAP:
                    try:
                        ItemClass = ITEM_CLASS_MAP[item_type]
                        item = ItemClass.from_dict(item_data)
                        self._catalog.add_item(item)
                        loaded_count += 1
                    except Exception as e:
                        print(f"WARNING: Skipping corrupted item '{item_data.get('title', 'Unknown')}' due to error: {e}")
                else:
                    print(f"WARNING: Skipping unknown item type: {item_type}")

            self._loan_manager.load_checkouts_from_dict(state.get("checkouts", {}))

            return f"System state loaded successfully. Restored {loaded_count} items."

        except json.JSONDecodeError as e:
            return f"ERROR: Failed to load state. File is corrupted/invalid JSON: {e}"
        except IOError as e:
            return f"ERROR: Failed to load state due to file operation error: {e}"
        except Exception as e:
            return f"ERROR: An unexpected error occurred during load: {e}"

    def import_items_from_csv(self, file_path: str) -> Tuple[int, str]:
        path = Path(file_path)
        if not path.exists():
            return 0, f"ERROR: Import file not found at {path}"

        imported_count = 0
        try:
            with open(path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row.get('type') in ITEM_CLASS_MAP and row.get('isbn'):
                        item_type = row['type']
                        ItemClass = ITEM_CLASS_MAP[item_type]
                        
                        try:
                            if item_type == "Book":
                                item = Book(row['title'], row['isbn'], int(row['year']), row['author'], row['genre'])
                            elif item_type == "DVD":
                                item = DVD(row['title'], row['isbn'], int(row['year']), row['director'])
                            elif item_type == "EBook":
                                item = EBook(row['title'], row['isbn'], int(row['year']), row['author'], float(row['file_size']))
                            
                            self._catalog.add_item(item)
                            imported_count += 1
                        except ValueError as ve:
                            print(f"WARNING: Skipping row due to incomplete/invalid data in model: {ve}")
                        except Exception as e:
                            print(f"WARNING: Skipping row due to creation error: {e}")

            return imported_count, f"Successfully imported {imported_count} items from {file_path}."

        except IOError as e:
            return 0, f"ERROR: Failed to read CSV file: {e}"
        except Exception as e:
            return 0, f"ERROR: An unexpected error occurred during import: {e}"

    def export_loan_report(self) -> str:
        checkouts = self._loan_manager.get_current_checkouts()
        if not checkouts:
            return "No items are currently checked out."

        report_lines = ["--- Current Loan Report ---"]
        report_lines.append(f"Generated: {date.today().isoformat()}")
        report_lines.append("-" * 30)

        for isbn, loan_data in checkouts.items():
            item = self._catalog.get_item(isbn)
            title = item.title if item else "Unknown Title"
            due_date = loan_data['due_date'].isoformat()
            
            report_lines.append(f"ISBN: {isbn}")
            report_lines.append(f"  Title: {title}")
            report_lines.append(f"  User: {loan_data['user']}")
            report_lines.append(f"  Due: {due_date}\n")

        try:
            with open(REPORT_FILE, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            return f"Loan report successfully exported to {REPORT_FILE}"
        except IOError as e:
            return f"ERROR: Failed to write export file: {e}"
