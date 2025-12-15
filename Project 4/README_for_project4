#  Python Library Management System

## Project Overview

This project implements a functional Command Line Interface (CLI) system for managing a small library's catalog and tracking item loans. It demonstrates core Python programming concepts including **Object-Oriented Programming (OOP)**, **Modularity**, **File Input/Output (I/O)**, and **Comprehensive Testing**.

The system uses Python's standard libraries (`json`, `csv`) for data handling and persistence.

##  How to Run the Application

### Prerequisites

This project requires only the **standard Python 3 installation**. No external libraries need to be installed.

### Execution Steps

1.  **Ensure Files are Present:** Make sure all files and the required `data/` folder are present in your project directory.
2.  **Run the Main Script:** Execute the main program from your terminal:

    ```bash
    python main_cli.py
    ```
3.  **Initial Load:** The program will first attempt to load the state from `data/library_state.json`. If it's a first run, it will automatically create the `data/` folder, the necessary data files (including a dummy import CSV), and load default items.
4.  **Use the Menu:** Follow the on-screen menu (1-7) to interact with the system (checkout, return, list items, save/exit).

##  System Architecture and Modularity

The project is designed using **Modularity** and **Separation of Concerns**, ensuring each file has a single, focused responsibility. 

| File Name | Responsibility | Key Python Concepts Demonstrated |
| :--- | :--- | :--- |
| **`library_model.py`** | Defines the core logic and data structures (`LibraryCatalog`, `LoanManager`, `LibraryItem` and its children). | **OOP (Classes, Inheritance, Polymorphism)** |
| **`persistence_manager.py`** | Handles all interactions with external files (`.json`, `.csv`, `.txt`). | **File I/O, `pathlib`, Exception Handling (`try/except`)** |
| **`main_cli.py`** | Manages the user interface, displays the menu, and processes user inputs. | **System Integration, Input/Output** |
| **`test_library.py`** | Contains unit and integration tests to verify the system's correctness. | **`unittest` module, Comprehensive Testing** |

### The `data/` Folder

This folder provides **Data Persistence** and organizational clarity by separating the application's source code from its generated or required data files.

* `library_state.json`: Saved state of the entire catalog and loan ledger (Permanent Memory).
* `import_items.csv`: Used for testing the required data import functionality.
* `loan_report.txt`: Generated output file for the loan report export feature.

##  Fulfillment of Technical Requirements

This project successfully implements the following key technical requirements required by the course:

### Object-Oriented Programming (OOP)

* **Inheritance:** `Book`, `DVD`, and `EBook` classes inherit from the abstract base class `LibraryItem`.
* **Polymorphism:** Each item type implements its own `calculate_loan_period()`, resulting in different checkout durations based on the item type (e.g., Book = 14 days, DVD = 3 days).
* **Composition:** `LibraryCatalog` and `LoanManager` manage and contain the various `LibraryItem` objects.

### Data Persistence & I/O

* **Save/Load State:** The system saves and loads the entire state (all items and all loans) using JSON encoding in `persistence_manager.py`.
* **Import Feature:** The `import_items_from_csv` method reads and integrates new data from a standard CSV file.
* **Export Feature:** The `export_loan_report` method generates a readable text report (`.txt`) of current loans.

### Testing and Best Practices

* **Comprehensive Testing:** `test_library.py` includes unit tests for individual classes and integration tests for combined workflows (checkout, return, persistence cycle).
* **`pathlib`:** The `persistence_manager.py` uses the modern `pathlib` module for organized, OS-agnostic file path construction.
* **Robustness:** **Exception Handling** (`try...except`) is used throughout the code to gracefully handle file errors (e.g., corrupted JSON state, invalid CSV data, or missing files).
