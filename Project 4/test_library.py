
import unittest
from datetime import date, timedelta
from pathlib import Path
import json
import csv

# Import all necessary components from your project files
from library_model import (
    LibraryItem, Book, DVD, EBook, 
    LibraryCatalog, LoanManager, ITEM_CLASS_MAP
)
# Import PersistenceManager and paths for system testing
from persistence_manager import PersistenceManager, DATA_DIR, REPORT_FILE


TEST_CSV_PATH = Path(DATA_DIR / "test_import.csv")
TEST_STATE_PATH = Path(DATA_DIR / "test_state.json")


def cleanup_test_files():
    if TEST_STATE_PATH.exists():
        TEST_STATE_PATH.unlink()
    if REPORT_FILE.exists():
        REPORT_FILE.unlink()
    if TEST_CSV_PATH.exists():
        TEST_CSV_PATH.unlink()
        
class TestLibraryModel(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()
        self.book = Book("Test Book", "111", 2020, "Author X", "Fiction")
        self.dvd = DVD("Test DVD", "222", 2021, "Director Y")
        
    def test_book_loan_period(self):
        self.assertEqual(self.book.calculate_loan_period(), 14)
        
    def test_add_item_to_catalog(self):
        self.catalog.add_item(self.book)
        self.assertEqual(self.catalog.get_item_count(), 1)
        self.assertIsInstance(self.catalog.get_item("111"), Book)
        
    def test_add_duplicate_item(self):
        self.catalog.add_item(self.book)
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.catalog.add_item(self.book)

    def test_check_out_unavailable(self):
        self.book.available = False
        due_date, message = self.book.check_out()
        self.assertIsNone(due_date)
        self.assertIn("already checked out", message)
        
class TestIntegration(unittest.TestCase):


    def setUp(self):
        self.catalog = LibraryCatalog()
        self.loan_manager = LoanManager(self.catalog)
        self.book_isbn = "B999"
        self.dvd_isbn = "D888"
        self.book = Book("Integration Test Book", self.book_isbn, 2020, "Author", "Fiction")
        self.dvd = DVD("Integration Test DVD", self.dvd_isbn, 2021, "Director")
        self.catalog.add_item(self.book)
        self.catalog.add_item(self.dvd)

    # 1. Test Catalog-to-LoanManager Data Flow
    def test_checkout_changes_catalog_availability(self):
        self.assertTrue(self.book.available)
        self.loan_manager.checkout_item("UserA", self.book_isbn)
        self.assertFalse(self.catalog.get_item(self.book_isbn).available)

    # 2. Test Polymorphic Loan Period
    def test_checkout_polymorphism_sets_correct_due_date(self):
        self.loan_manager.checkout_item("UserB", self.book_isbn) # 14 days
        self.loan_manager.checkout_item("UserC", self.dvd_isbn) # 3 days
        
        book_loan_data = self.loan_manager.get_current_checkouts()[self.book_isbn]
        dvd_loan_data = self.loan_manager.get_current_checkouts()[self.dvd_isbn]
        
        expected_book_date = date.today() + timedelta(days=14)
        expected_dvd_date = date.today() + timedelta(days=3)
        
        self.assertEqual(book_loan_data['due_date'], expected_book_date)
        self.assertEqual(dvd_loan_data['due_date'], expected_dvd_date)

    # 3. Test Loan-Return-Fee Cycle
    def test_return_item_with_late_fee(self):
        self.loan_manager.checkout_item("UserD", self.book_isbn)
        result = self.loan_manager.return_item(self.book_isbn, days_late=5) # $2.50 fee
        
        self.assertIn("$2.50", result)
        self.assertTrue(self.book.available)
        self.assertNotIn(self.book_isbn, self.loan_manager.get_current_checkouts())

    # 4. Test LoanManager Handles Unknown ISBN
    def test_checkout_unknown_isbn(self):
        result = self.loan_manager.checkout_item("FailUser", "0000")
        self.assertIn("Error: Item not found.", result)

    # 5. Test State Serialization Interface (Persistence Prep)
    def test_checkouts_to_dict_format(self):
        today = date.today()
        self.book.available = False
        self.loan_manager._checkouts = {self.book_isbn: {"user": "TestUser", "due_date": today}}
        
        data = self.loan_manager.checkouts_to_dict()
        self.assertEqual(data[self.book_isbn]['due_date'], today.isoformat())

class TestPersistence(unittest.TestCase):

    
    def setUp(self):
        cleanup_test_files()
        self.catalog = LibraryCatalog()
        self.loan_manager = LoanManager(self.catalog)
        self.persistence = PersistenceManager(self.catalog, self.loan_manager)
        self.persistence.STATE_FILE = TEST_STATE_PATH
        
        # Populate the system state
        self.book_isbn = "9000"
        self.dvd_isbn = "8000"
        self.catalog.add_item(Book("Persist Book", self.book_isbn, 2020, "P. Author", "SciFi"))
        self.catalog.add_item(DVD("Persist DVD", self.dvd_isbn, 2021, "D. Director"))
        self.loan_manager.checkout_item("SysUser", self.book_isbn)

    def tearDown(self):
        cleanup_test_files()

    # 1. Full Save/Load Cycle
    def test_full_save_and_load_cycle(self):
        initial_item_count = self.catalog.get_item_count()
        initial_loan_count = len(self.loan_manager.get_current_checkouts())
        self.persistence.save_state()
        self.assertTrue(TEST_STATE_PATH.exists())

        new_catalog = LibraryCatalog()
        new_loan_manager = LoanManager(new_catalog)
        new_persistence = PersistenceManager(new_catalog, new_loan_manager)
        new_persistence.STATE_FILE = TEST_STATE_PATH

        new_persistence.load_state()

        self.assertEqual(new_catalog.get_item_count(), initial_item_count)
        self.assertEqual(len(new_loan_manager.get_current_checkouts()), initial_loan_count)
        
        restored_book = new_catalog.get_item(self.book_isbn)
        self.assertIsInstance(restored_book, Book)
        self.assertFalse(restored_book.available)
        self.assertIn("SysUser", new_loan_manager.get_current_checkouts()[self.book_isbn]['user'])


    # 2. Import & Catalog Integration Workflow
    def test_import_from_csv_workflow(self):
        with open(TEST_CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["type", "title", "isbn", "year", "author", "genre", "director", "file_size"])
            writer.writerow(["Book", "Test Import 1", "I111", "2023", "Importer A", "Test", "", ""])
            writer.writerow(["DVD", "Test Import 2", "I222", "2024", "", "", "Importer B", ""])
            writer.writerow(["Book", "Bad Data", "I333", "YearFail", "Author C", "Test", "", ""])

        initial_count = self.catalog.get_item_count()
        imported_count, message = self.persistence.import_items_from_csv(str(TEST_CSV_PATH))
        
        self.assertEqual(imported_count, 2)
        self.assertEqual(self.catalog.get_item_count(), initial_count + 2)
        self.assertIsInstance(self.catalog.get_item("I222"), DVD)


    # 3. Reporting Workflow (Export)
    def test_export_loan_report_workflow(self):
        self.loan_manager.checkout_item("ReportUser", self.dvd_isbn)
        self.persistence.export_loan_report()
        self.assertTrue(REPORT_FILE.exists())
        
        with open(REPORT_FILE, 'r') as f:
            content = f.read()
            
        self.assertIn("Current Loan Report", content)
        self.assertIn(self.dvd_isbn, content)

    # 4. Robustness Test: Load Corrupted State (Required Error Handling)
    def test_load_corrupted_state(self):
        with open(TEST_STATE_PATH, 'w') as f:
            f.write("{This is invalid JSON") 

        result = self.persistence.load_state()
        
        self.assertIn("File is corrupted/invalid JSON", result)
        self.assertEqual(self.catalog.get_item_count(), 0)
        self.assertEqual(len(self.loan_manager.get_current_checkouts()), 0)


# Run the tests
if __name__ == '__main__':

    if not DATA_DIR.exists():
        DATA_DIR.mkdir()
    
    # Run the tests
    print("\n--- Running Comprehensive Library Tests ---")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    print("--- Test Suite Complete ---")


    cleanup_test_files()
