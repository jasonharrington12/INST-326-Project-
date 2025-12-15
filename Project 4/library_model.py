import abc
from datetime import date, timedelta, datetime # datetime is now imported for strptime
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class LibraryItem(ABC):
    
    def __init__(self, title: str, isbn: str, year: int, available: bool = True):
        if not all([title, isbn, year]):
            raise ValueError("Title, ISBN, and Year must be provided.")
        self.title = title
        self.isbn = isbn
        self.year = year
        self.available = available

    def __str__(self):
        status = "Available" if self.available else "Checked Out"
        return f"{self.__class__.__name__}: '{self.title}' ({self.year}) - {status}"

    @abstractmethod
    def calculate_loan_period(self) -> int:
        pass

    def check_out(self):
        if not self.available:
            return None, "Item is already checked out."

        loan_days = self.calculate_loan_period()
        self.available = False
        due_date = date.today() + timedelta(days=loan_days)
        return due_date, f"'{self.title}' checked out. Due date: {due_date.isoformat()} ({loan_days} days)."

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "title": self.title,
            "isbn": self.isbn,
            "year": self.year,
            "available": self.available,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        raise NotImplementedError("Subclasses must implement from_dict.")


class Book(LibraryItem):
    
    def __init__(self, title, isbn, year, author, genre, available=True):
        super().__init__(title, isbn, year, available)
        self.author = author
        self.genre = genre

    def calculate_loan_period(self) -> int:
        return 14

    def to_dict(self):
        data = super().to_dict()
        data.update({"author": self.author, "genre": self.genre})
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data['title'], data['isbn'], data['year'], data['author'], 
                   data['genre'], data['available'])

class DVD(LibraryItem):
    
    def __init__(self, title, isbn, year, director, available=True):
        super().__init__(title, isbn, year, available)
        self.director = director

    def calculate_loan_period(self) -> int:
        return 3

    def to_dict(self):
        data = super().to_dict()
        data.update({"director": self.director})
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data['title'], data['isbn'], data['year'], data['director'], 
                   data['available'])

class EBook(LibraryItem):
    
    def __init__(self, title, isbn, year, author, file_size, available=True):
        super().__init__(title, isbn, year, available)
        self.author = author
        self.file_size = file_size

    def calculate_loan_period(self) -> int:
        return 28
    
    def to_dict(self):
        data = super().to_dict()
        data.update({"author": self.author, "file_size": self.file_size})
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data['title'], data['isbn'], data['year'], data['author'], 
                   data['file_size'], data['available'])

# Dictionary to map item type string to its class for deserialization
ITEM_CLASS_MAP = {
    "Book": Book,
    "DVD": DVD,
    "EBook": EBook,
}

class LibraryCatalog:
    
    def __init__(self):
        self._items: Dict[str, LibraryItem] = {}

    def add_item(self, item: LibraryItem):
        if item.isbn in self._items:
            raise ValueError(f"Item with ISBN {item.isbn} already exists.")
        self._items[item.isbn] = item

    def get_item(self, isbn) -> LibraryItem | None:
        return self._items.get(isbn)

    @property
    def all_items(self) -> List[LibraryItem]:
        return list(self._items.values())

    def get_item_count(self) -> int:
        return len(self._items)


class LoanManager:
    
    def __init__(self, catalog: LibraryCatalog):
        self._catalog = catalog
        self._checkouts: Dict[str, Dict] = {} 

    def checkout_item(self, user_name: str, isbn: str):
        item = self._catalog.get_item(isbn)
        if not item:
            return "Error: Item not found."

        # Polymorphic call
        due_date, message = item.check_out()

        if due_date:
            self._checkouts[isbn] = {"user": user_name, "due_date": due_date}
            return f"{message} User: {user_name}"
        return message

    def return_item(self, isbn: str, days_late: int = 0, fee_per_day: float = 0.50):
        item = self._catalog.get_item(isbn)
        if not item:
            return "Error: Item not found."
        
        if isbn not in self._checkouts:
             if not item.available:
                 item.available = True
                 return f"'{item.title}' returned. Was not tracked in LoanManager, corrected item status."
             return "Item was not checked out."

        item.available = True
        user_name = self._checkouts.pop(isbn, {}).get("user", "Unknown")

        fee = max(days_late * fee_per_day, 0)
        return f"{user_name} returned '{item.title}'. Late fee: ${fee:.2f}"

    def get_current_checkouts(self) -> Dict[str, Dict]:
        return self._checkouts

    def checkouts_to_dict(self) -> Dict[str, Dict]:
        serializable_checkouts = {}
        for isbn, loan_data in self._checkouts.items():
            serializable_checkouts[isbn] = {
                "user": loan_data["user"],
                "due_date": loan_data["due_date"].isoformat()
            }
        return serializable_checkouts

    def load_checkouts_from_dict(self, data: Dict[str, Dict]):
        self._checkouts = {}
        for isbn, loan_data in data.items():
            try:
                loan_date = datetime.strptime(loan_data["due_date"], '%Y-%m-%d').date()
                self._checkouts[isbn] = {
                    "user": loan_data["user"],
                    "due_date": loan_date
                }
            except Exception as e:
                print(f"Error loading checkout for {isbn}: {e}")
                continue
