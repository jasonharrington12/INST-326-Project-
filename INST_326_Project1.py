books = []

def add_book(title, author, year, isbn):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "isbn": isbn
    }
    books.append(book)

def display_books():
    for book in books:
        print(book)

def search_books(query):
    """Search for books by title or author (case-insensitive)"""
    query = query.lower()
    results = []
    for book in books:
        if query in book["title"].lower() or query in book["author"].lower():
            results.append(book)
    return results

def get_book(isbn):
    """Get a specific book by ISBN"""
    for book in books:
        if book["isbn"] == isbn:
            return book
    return None

def delete_book(book_id):
  """ removes book from catalog if lost, damaged, or outdated"""
  for book in books:
    if book["id"] == book_id:
      books.remove(book)
      return True
  return False

  

# Add books
add_book("The Hobbit", "J.R.R. Tolkien", 1937, "978-0-345-33968-3")
add_book("1984", "George Orwell", 1949, "978-0-452-28423-4")

# Display all books
display_books()

# Search and retrieve books
print("\nSearch results for 'tolkien':")
print(search_books("tolkien"))

print("\nGet book by ISBN:")
print(get_book("978-0-452-28423-4"))


### Movies


import pandas as pd

def analyze_movies():
    """Analyzes movie ratings."""

    # Movie data
    movies = {
        'title': ['Movie A', 'Movie B', 'Movie C', 'Movie D'],
        'genre': ['Action', 'Comedy', 'Action', 'Comedy'],
        'rating': [7.5, 8.0, 9.0, 7.0]
    }
    df = pd.DataFrame(movies)

    print("Movies:")
    print(df)
    print("\nAverage by Genre:")
    print(df.groupby('genre')['rating'].mean())

analyze_movies()


## Book Rating

# Library Book Rating Program

# List of books in the library
library = [
    {"title": "1984", "rating": None},
    {"title": "To Kill a Mockingbird", "rating": None},
    {"title": "The Great Gatsby", "rating": None},
    {"title": "Moby Dick", "rating": None},
]

def rate_book(library):
    """Allows the user to rate books in the library."""
    print("Welcome to the Library Rating System!")
    print("Available books:\n")

    # Display all books
    for i, book in enumerate(library, start=1):
        print(f"{i}. {book['title']}")

    # Ask user which book to rate
    choice = int(input("\nEnter the number of the book you want to rate: "))
    if 1 <= choice <= len(library):
        rating = float(input("Enter your rating (1 to 5): "))

        # Validate rating
        if 1 <= rating <= 5:
            library[choice - 1]["rating"] = rating
            print(f"\nYou rated '{library[choice - 1]['title']}' a {rating}/5.")
        else:
            print("Invalid rating! Please enter a value between 1 and 5.")
    else:
        print("Invalid choice!")

def show_ratings(library):
    """Displays all books with their ratings."""
    print("\nBook Ratings:")
    for book in library:
        rating = book["rating"] if book["rating"] is not None else "Not rated"
        print(f"- {book['title']}: {rating}")

# Run the program
rate_book(library)
show_ratings(library)


# Stevens code review
# The overall structure is clear — each section (books, movies, ratings) is logically separated and well-commented.
# The delete_book() function references book["id"], but no "id" field exists in the add_book() function — consider using isbn instead.
# The rate_book() function’s input() calls make it interactive but limit automation or testing maybe change it a bit for further scalability?
# Consistent use of docstrings is great; adding return values or type hints would further improve clarity and maintainability

