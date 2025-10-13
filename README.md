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
