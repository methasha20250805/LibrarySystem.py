from Validations import validate_bookid, validate_studentid, validate_date
from StoreData import load_books, save_books, load_students,load_transactions,append_transactions

def issue_book():
    print("Issue Book")
    books = load_books()
    students = load_students()
    transactions = load_transactions()

    while True:
        bookid = input("Enter book ID: ")
        if not validate_bookid(bookid):
            print("Invalid book ID")
            continue
        book = next((b for b in books if b["bookID"] == bookid), None)
        if not book:
            print("No book found")
            continue
        break

    while True:
        studentid = input("Enter student ID: ")
        if not validate_studentid(studentid):
            print("Invalid student ID")
            continue
        student = next((s for s in students if s["studentID"] == studentid), None)
        if not student:
            print("No student found")
            continue
        break

    if _already_holds_book(transactions, bookid, studentid):
        print(f"Student '{student['firstName']}' has already been issued Book ID '{bookid}'.")
        print("Multiple copies of the same book cannot be issued to the same student.")
        return

    if int(book["availability"]) <=0:
        print(f"Book '{book['title']}' is not available right now.")
        return

    while True:
        date_str = input("Enter Issue Date (DD/MM/YYYY): ")
        if not validate_date(date_str):
            print("Invalid date! Use DD/MM/YYYY format.")
            continue
        break

    book["availability"] = str(int(book["availability"]) - 1)
    save_books(books)

    append_transactions({
        "bookID": bookid,
        "studentID": studentid,
        "date": date_str,
        "type": "1"
    })

    print(f"Book '{book['title']}' successfully issued to {student['firstName']} on {date_str}.")
    print(f"Remaining availability: {book['availability']}/{book['copies']}")

def _already_holds_book(transactions: list, book_id: str, student_id: str) -> bool:
    count = 0
    for t in transactions:
        if t["bookID"] == book_id and t["studentID"] == student_id:
            if t["type"] == "1":
                count += 1
            elif t["type"] == "2":
                count = max(0, count - 1)
    return count > 0