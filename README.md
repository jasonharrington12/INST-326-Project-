# INST-326-Project-

ReadMe file for For INST_326_Project1.py
 Library and Movie Programs
 This project contains Python programs for managing books, analyzing movies, and allowing users to
 rate library books. Each program demonstrates basic Python concepts such as lists, dictionaries,
 functions, loops, and user input.
 1. Book Management
 Features:- Add books to a catalog.- Display all books.- Search books by title or author (case-insensitive).- Retrieve a book by ISBN.- Delete a book by ID.
 Example Usage:
 # Add books
 add_book("The Hobbit", "J.R.R. Tolkien", 1937, "978-0-345-33968-3")
 add_book("1984", "George Orwell", 1949, "978-0-452-28423-4")
 # Display books
 display_books()
 # Search books
 search_books("tolkien")
 # Get book by ISBN
 get_book("978-0-452-28423-4")
 2. Movie Analysis
 Features:- Analyze movie ratings using pandas.- Compute the average rating for each genre.
 Example Usage:
 analyze_movies()
 How It Works:
 1. Movie data is stored in a dictionary with title, genre, and rating.
 2. Data is converted to a pandas DataFrame.
 3. Average ratings by genre are calculated using groupby.
 3. Library Book Rating
Features:- Allows users to rate books from a library.- Displays all books and their ratings.
 Example Usage:
 rate_book(library)
 show_ratings(library)
 How It Works:
 1. The program lists all available books.
 2. Users select a book to rate.
 3. Users input a rating between 1 and 5.
 4. The program updates the rating and displays all books with their ratings.


# Library Management System
ReadMe file for 311_project.ipynb
A simple Python library management system with functions for managing books, calculating late fees, and handling checkouts.

## Features

- **Late Fee Calculation**: Calculate overdue fees based on days late
- **Genre Search**: Find books by their genre
- **ISBN Lookup**: Search for books using ISBN
- **Checkout System**: Check out and return books

## Functions

### `calculate_late_fee(days_late, fee_per_day=0.25)`
Calculates the late fee for overdue books.

**Parameters:**
- `days_late` (int): Number of days the book is overdue
- `fee_per_day` (float, optional): Fee charged per day (default: $0.25)

**Returns:**
- `float`: Total late fee amount
- `str`: Error message if invalid input

**Example:**
```python
fee = calculate_late_fee(10)  # Returns 2.5
fee = calculate_late_fee(5, fee_per_day=0.50)  # Returns 2.5
```

### `find_books_by_genre(genre, book_list)`
Finds all books matching a specific genre.

**Parameters:**
- `genre` (str): Genre to search for (case-insensitive)
- `book_list` (list): List of book dictionaries with 'genre' key

**Returns:**
- `list`: List of matching book dictionaries

**Example:**
```python
books = [
    {'title': 'Book A', 'genre': 'Fiction'},
    {'title': 'Book B', 'genre': 'Science'}
]
fiction_books = find_books_by_genre('fiction', books)
```

### `find_book_by_isbn(isbn, book_list)`
Locates a book using its ISBN.

**Parameters:**
- `isbn` (str): ISBN number to search for
- `book_list` (list): List of book dictionaries with 'isbn' key

**Returns:**
- `dict`: Book dictionary if found
- `str`: "Book not found with that ISBN." if not found

**Example:**
```python
book = find_book_by_isbn('978-0-123456-78-9', book_list)
```

### `check_out_book(book_title, user_name)`
Simulates checking out a book to a user.

**Parameters:**
- `book_title` (str): Title of the book
- `user_name` (str): Name of the user checking out the book

**Returns:**
- `str`: Confirmation message

**Example:**
```python
message = check_out_book('Python Programming', 'John Doe')
# Returns: "Python Programming checked out by John Doe."
```

### `return_book(book_title, user_name)`
Simulates returning a book from a user.

**Parameters:**
- `book_title` (str): Title of the book
- `user_name` (str): Name of the user returning the book

**Returns:**
- `str`: Confirmation message

**Example:**
```python
message = return_book('Python Programming', 'John Doe')
# Returns: "Python Programming returned by John Doe."
```

## Usage

```python
# Sample book list structure
book_list = [
    {
        'title': 'The Great Gatsby',
        'genre': 'Fiction',
        'isbn': '978-0-7432-7356-5'
    },
    {
        'title': 'A Brief History of Time',
        'genre': 'Science',
        'isbn': '978-0-553-10953-5'
    }
]

# Calculate a late fee
fee = calculate_late_fee(7)  # $1.75 for 7 days late

# Find all fiction books
fiction = find_books_by_genre('Fiction', book_list)

# Look up a specific book
book = find_book_by_isbn('978-0-7432-7356-5', book_list)

# Check out and return books
check_out_book('The Great Gatsby', 'Alice Smith')
return_book('The Great Gatsby', 'Alice Smith')
```

## Notes

- The `find_books_by_genre()` function performs case-insensitive matching
- Late fees cannot be calculated for negative days
- Book list dictionaries should include appropriate keys ('genre', 'isbn', etc.) for the functions to work properly

