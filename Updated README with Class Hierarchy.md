# Library Management System - Class Hierarchy

## Overview
This system demonstrates object-oriented design principles through a library management application that handles books, DVDs, and eBooks.

## Class Hierarchy

### Abstract Base Class
**`LibraryItem` (ABC)**
- Root of the inheritance hierarchy
- Defines common attributes: `title`, `isbn`, `year`, `available`
- Abstract method: `calculate_loan_period()` - must be implemented by subclasses
- Concrete methods: `check_out()`, `__str__()`

### Derived Classes (Inherit from LibraryItem)

#### **`Book`**
- **Extends:** `LibraryItem`
- **Additional attributes:** `author`, `genre`
- **Loan period:** 14 days

#### **`DVD`**
- **Extends:** `LibraryItem`
- **Additional attributes:** `director`
- **Loan period:** 3 days

#### **`EBook`**
- **Extends:** `LibraryItem`
- **Additional attributes:** `author`, `file_size`
- **Loan period:** 28 days

### Composition Classes

#### **`LibraryCatalog`**
- Manages a collection of `LibraryItem` objects
- Uses composition (has-a relationship) with `LibraryItem`
- **Methods:** `add_item()`, `get_item()`, `all_items` property

#### **`LoanManager`**
- Manages checkout and return operations
- Uses composition (has-a relationship) with `LibraryCatalog`
- **Methods:** `checkout_item()`, `return_item()`
- Tracks active loans and calculates late fees

## Key Design Patterns

| Pattern | Description |
|---------|-------------|
| **Inheritance** | All item types inherit from `LibraryItem` |
| **Polymorphism** | Each derived class implements `calculate_loan_period()` differently |
| **Composition** | `LoanManager` contains a `LibraryCatalog`, which contains multiple `LibraryItem` objects |
| **Abstraction** | `LibraryItem` defines the contract that all library items must follow |

## Class Diagram
```
LibraryItem (ABC)
    ├── Book
    ├── DVD
    └── EBook

LibraryCatalog
    └── contains: List[LibraryItem]

LoanManager
    └── contains: LibraryCatalog
```

## Usage Example
```python
# Initialize system
catalog = LibraryCatalog()
loan_manager = LoanManager(catalog)

# Add items
book = Book("1984", "9780451524935", 1949, "George Orwell", "Dystopian")
catalog.add_item(book)

# Checkout (polymorphic behavior - 14 days for books)
loan_manager.checkout_item("Alice", "9780451524935")

# Return with late fee calculation
loan_manager.return_item("9780451524935", days_late=10)
```
