from library_model import LibraryCatalog, LoanManager, Book, DVD, EBook
from persistence_manager import PersistenceManager
from pathlib import Path
import csv

class LibraryCLI:

    def __init__(self):
        self.catalog = LibraryCatalog()
        self.loan_manager = LoanManager(self.catalog)
        self.persistence = PersistenceManager(self.catalog, self.loan_manager)
        
        print("\n--- System Initialization ---")
        print(self.persistence.load_state())
        
        if self.catalog.get_item_count() == 0:
            print("Catalog is empty. Adding demo items.")
            self._add_demo_items()
        
        print(f"System ready with {self.catalog.get_item_count()} items.")

    def _add_demo_items(self):

        try:
            self.catalog.add_item(Book("1984", "9780451524935", 1949, "George Orwell", "Dystopian"))
            self.catalog.add_item(DVD("2001: A Space Odyssey", "D9999", 1968, "Stanley Kubrick"))
            self.catalog.add_item(EBook("Python Guide", "E8888", 2023, "G. Programmer", 10.5))
            self.catalog.add_item(Book("The Great Gatsby", "9780743273565", 1925, "F. Scott Fitzgerald", "Classic"))
        except ValueError:
            pass

    def run(self):

        menu = (
            "\n--- Library Menu ---\n"
            "1. List All Items\n"
            "2. Checkout Item\n"
            "3. Return Item\n"
            "4. Import Items (CSV)\n"
            "5. Export Loan Report\n"
            "6. Save State & Exit\n"
            "7. Exit Without Saving\n"
            "--------------------"
        )
        
        while True:
            print(menu)
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.list_items()
            elif choice == '2':
                self.handle_checkout()
            elif choice == '3':
                self.handle_return()
            elif choice == '4':
                self.handle_import()
            elif choice == '5':
                self.handle_export()
            elif choice == '6':
                print(self.persistence.save_state())
                break
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")

    def list_items(self):
        if not self.catalog.all_items:
            print("The catalog is currently empty.")
            return

        print("\n--- Catalog Items ---")
        for item in self.catalog.all_items:
            print(f"- {item}")
        
        print("\n--- Current Loans ---")
        loans = self.loan_manager.get_current_checkouts()
        if not loans:
            print("No items currently on loan.")
            return
        for isbn, data in loans.items():
             print(f"ISBN: {isbn} | User: {data['user']} | Due: {data['due_date'].isoformat()}")


    def handle_checkout(self):
        isbn = input("Enter ISBN to checkout: ").strip()
        user = input("Enter user name: ").strip()
        if not user:
            print("User name cannot be empty.")
            return
        
        result = self.loan_manager.checkout_item(user, isbn)
        print(f"\n{result}")

    def handle_return(self):
        isbn = input("Enter ISBN to return: ").strip()
        try:
            days_late = int(input("Enter days late (0 if on time): ").strip() or 0)
        except ValueError:
            print("Invalid input for days late. Assuming 0.")
            days_late = 0

        result = self.loan_manager.return_item(isbn, days_late=days_late)
        print(f"\n{result}")

    def handle_import(self):

        import_path = Path("data/import_items.csv")
        if not import_path.exists():
            self._create_dummy_csv(import_path)

        print(f"\nAttempting to import from: {import_path}")
        
        count, message = self.persistence.import_items_from_csv(str(import_path))
        print(message)
        if count > 0:
            print(f"Import successful. Total items now: {self.catalog.get_item_count()}")

    def handle_export(self):

        print("\n--- Exporting Loan Report ---")
        result = self.persistence.export_loan_report()
        print(result)

    def _create_dummy_csv(self, file_path: Path):

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["type", "title", "isbn", "year", "author", "genre", "director", "file_size"])
                writer.writerow(["Book", "The Hobbit", "9780345339683", "1937", "J.R.R. Tolkien", "Fantasy", "", ""])
                writer.writerow(["DVD", "Pulp Fiction", "D4444", "1994", "", "", "Quentin Tarantino", ""])
            print(f"Created dummy import CSV at {file_path}. Run import to add these items.")
        except Exception as e:
            print(f"Could not create dummy CSV: {e}")


if __name__ == "__main__":
    cli = LibraryCLI()
    cli.run()
