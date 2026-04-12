from Validations import (validate_bookid, validate_isbn, validate_title, validate_copies, validate_price)
from StoreData import (load_books, save_books)

def booksmenu():
    while True:
        print("Books Menu")
        print("1. Add Book")
        print("2. Edit / Update Book")
        print("3.Search book")
        print("4. View all books")
        print("5. Back to main menu")

        choice = input("Enter your choice [1 -5]: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            edit_book_menu()
        elif choice == "3":
            search_book_menu()
        elif choice == "4":
            view_book()
        elif choice == "5":
            break
        else:
            print("Invalid Choice")

def add_book():
    print("Add Book")
    books = load_books()
    while True:
        book_id = input("Enter Book ID(2 letters + 2 digits, eg:AB12): ").upper()
        if not validate_bookid(book_id):
            print("Invalid Book ID. Must be 2 letters followed by 2 digits")
            continue
        if any(b["bookID"].upper() == book_id for b in books):
            print("Book ID already exists")
            continue
        break

    while True:
        isbn = input("Enter ISBN-13 number: ")
        if not validate_isbn(isbn):
            print("Invalid ISBN-13 number. Check digit validation failed.")
            continue
        if any(i["isbnNumber"]== isbn for i in books):
                print("A book with that ISBN number already exists")
                continue
        break

    while True:
        title = input("Enter Book Title(maximum 20 characters): ").strip()
        if not validate_title(title):
            print("Invalid Book Title.Letters only, maximum 20 characters.")
            continue
        break

    while True:
        author = input("Enter Author: ")
        if not author:
            print("Author cannot be empty.")
            continue
        break

    while True:
        copies_str = input("Enter number of copies (1 or 2): ")
        if not validate_copies(copies_str):
            print("Should be less than 2 copies.")
            continue
        break

    while True:
        price_str = input("Enter Price (with 2 decimal places): ")
        if not validate_price(price_str):
            print("Enter price to 2 decimal places.(eg: 20.00)")
            continue
        break

    copies = int(copies_str)
    new_book = {
        "bookID": book_id,
        "title": title,
        "isbnNumber": isbn,
        "author": author,
        "copies": str(copies),
        "availability": str(copies),
        "price": price_str
    }

    books.append(new_book)
    save_books(books)
    print("Book Added Successfully.")

def edit_book_menu():
    print("Edit / Update Book Details")
    print("1. Search by bookID")
    print("2. Search by book title")
    print("3. Search by ISBN-13 number")

    option = input("Enter your choice [1 -3]: ")
    books = load_books()

    if option == "1":
        bookid = input("Enter Book ID: ")
        if not validate_bookid(bookid):
            print("Invalid bookID")
            return
        results = [b for b in books if b["bookID"] == bookid]
    elif option == "2":
        keyword = input("Enter Book Title: ")
        results = [b for b in books if keyword.lower() in b["title"].lower()]
    elif option == "3":
        isbn = input("Enter ISBN-13 number: ")
        if not validate_isbn(isbn):
            print("Invalid ISBN-13 number.")
            return
        results = [b for b in books if b["isbnNumber"] == isbn]
    else:
        print("Invalid Choice")
        return

    if not results:
        print("No books found.")
        return

    display_books(results)

    book_id = input("Enter Book ID to edit: ")
    if not book_id:
        print("Edit cancelled.")
        return
    book = next((b for b in books if b["bookID"] == book_id), None)
    if not book:
        print("Book not found.")
        return

    print(f"Editing Book: {book["bookID"]} - {book["title"]}")
    print("Press Enter to keep the current value.")

    while True:
        value = input(f"ISBN-13 [{book['isbnNumber']}]: ")
        if value == "":
            break
        if validate_isbn(value):
            book["isbnNumber"] = value
            break
        print("Invalid ISBN-13 number.")

    while True:
        value = input(f"Title [{book['title']}]: ")
        if value == "":
            break
        if validate_title(value):
            book["title"] = value
            break
        print("Invalid title. Letters only, max 20 characters.")

    value = input(f"Author [{book['author']}]: ")
    if value:
        book["author"] = value

    while True:
        value = input(f"Copies [{book['copies']}] (1 or 2): ")
        if value == "":
            break
        if validate_copies(value):
            new_copies = int(value)
            issued = int(book["copies"]) - int(book["availability"])
            book["copies"] = str(new_copies)
            book["availability"] = str(max(0, new_copies - issued))
            break
        print("Invalid. Copies must be 1 or 2.")

    while True:
        value = input(f"Price [{book['price']}]: ")
        if value == "":
            break
        if validate_price(value):
            book["price"] = value
            break
        print("Invalid price. Must have exactly 2 decimal places (e.g. 20.00).")

    save_books(books)
    print("Book updated and saved Successfully.")

def search_book_menu():
    print("Search books")
    print("1. Search by Book ID")
    print("2. Search by Book Title")
    print("3. Search by ISBN-13 Number")

    option = input("Enter your choice [1 -3]: ")
    books = load_books()

    if option == "1":
        book_id = input("Enter Book ID: ")
        if not validate_bookid(book_id):
            print("Invalid bookID")
            return
        results = [b for b in books if b["bookID"] == book_id]
    elif option == "2":
        keyword = input("Enter title keyword: ")
        if not keyword:
            print("No keyword entered.")
            return
        results = [b for b in books if keyword.lower() in b["title"].lower()]

    elif option == "3":
        isbn = input("Enter ISBN-13 number: ")
        if not validate_isbn(isbn):
            print("Invalid ISBN-13 number.")
            return
        results = [b for b in books if b["isbnNumber"] == isbn]

    else:
        print("Invalid Choice")
        return
    if not results:
        print("No books found.")
        return

    display_books(results)

def view_book():
    print("View all books")
    books = load_books()

    if not books:
        print("No books found in the system.")
        return

    display_books(books)
    total_copies    = sum(int(b["copies"])       for b in books)
    total_available = sum(int(b["availability"]) for b in books)
    total_issued    = total_copies - total_available

    print(f"Total copies : {total_copies}")
    print(f"Available    : {total_available}")
    print(f"Issued out   : {total_issued}")

def display_books(books):
    print(f"{'ID':<6} {'Title':<22} {'ISBN-13':<18} {'Author':<20} {'Copies':<7} {'Availability':<15} {'Price'}")
    print("-" * 105)
    for b in books:
        print(f"{b['bookID']:<6} {b['title']:<22} {b['isbnNumber']:<18} "
              f"{b['author']:<20} {b['copies']:<7} {b['availability']:<15} {b['price']}")
    print(f"Total: {len(books)} book(s) found.")
