from abc import ABC, abstractmethod
from datetime import date, timedelta


# MODELS


class LibraryItem(ABC):
    def __init__(self, title: str, isbn: str, year: int, available: bool = True):
        if not all([title, isbn, year]):
            raise ValueError("Title, ISBN, and year are required.")
        self.title = title
        self.isbn = isbn
        self.year = year
        self.available = available

    @abstractmethod
    def calculate_loan_period(self) -> int:
        pass

    def check_out(self):
        if not self.available:
            return None, "Item already checked out."

        self.available = False
        due_date = date.today() + timedelta(days=self.calculate_loan_period())
        return due_date, due_date.isoformat()

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "title": self.title,
            "isbn": self.isbn,
            "year": self.year,
            "available": self.available,
            **self.__dict__
        }


class Book(LibraryItem):
    def __init__(self, title, isbn, year, author, genre, available=True):
        super().__init__(title, isbn, year, available)
        self.author = author
        self.genre = genre

    def calculate_loan_period(self):
        return 14


class DVD(LibraryItem):
    def __init__(self, title, isbn, year, director, available=True):
        super().__init__(title, isbn, year, available)
        self.director = director

    def calculate_loan_period(self):
        return 3


class EBook(LibraryItem):
    def __init__(self, title, isbn, year, author, file_size, available=True):
        super().__init__(title, isbn, year, available)
        self.author = author
        self.file_size = file_size

    def calculate_loan_period(self):
        return 28



# SYSTEM CLASSES


class LibraryCatalog:
    def __init__(self):
        self.items = {}

    def add_item(self, item: LibraryItem):
        if item.isbn in self.items:
            raise ValueError("Duplicate ISBN.")
        self.items[item.isbn] = item

    def get_item(self, isbn):
        return self.items.get(isbn)

    def all_items(self):
        return list(self.items.values())


class LoanManager:
    def __init__(self, catalog: LibraryCatalog):
        self.catalog = catalog
        self.checkouts = {}

    def checkout_item(self, user, isbn):
        item = self.catalog.get_item(isbn)
        if not item:
            return "Item not found."

        due_date, msg = item.check_out()
        if due_date:
            self.checkouts[isbn] = {"user": user, "due_date": due_date.isoformat()}
            return f"Checked out to {user}, due {msg}"
        return msg

    def return_item(self, isbn, days_late=0, fee_per_day=0.5):
        item = self.catalog.get_item(isbn)
        if not item or item.available:
            return "Invalid return."

        item.available = True
        self.checkouts.pop(isbn, None)
        fee = max(days_late * fee_per_day, 0)
        return f"Returned. Late fee: ${fee:.2f}"
