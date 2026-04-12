from Validations import validate_bookid, validate_studentid, validate_date
from StoreData import load_books,save_books,load_students,load_transactions,append_transactions
from datetime import datetime
#return book
def return_book():
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
#Check whether book already is there
    if not _currently_holds_book(transactions, bookid, studentid):
        print(f"Book '{book['title']}' has already been returned or was never issued to "
              f"student '{student['firstName']}'.")
        return
# to check whether return data is after the issue date
    def _get_issue_date(transactions: list, bookid: str, studentid: str):
        issue_date = None
        for t in transactions:
            if t["bookID"] == bookid and t["studentID"] == studentid and t["type"] == "1":
                d = datetime.strptime(t["date"], "%d/%m/%Y")
                if issue_date is None or d > issue_date:
                    issue_date = d
        return issue_date

    issue_date = _get_issue_date(transactions, bookid, studentid)
    while True:
        date_str = input("Enter Return Date (DD/MM/YYYY): ")
        if not validate_date(date_str):
            print("Invalid date! Use DD/MM/YYYY format.")
            continue
        if issue_date and datetime.strptime(date_str, "%d/%m/%Y") < issue_date:
            print(f"Return date cannot be before the issue date ({issue_date.strftime('%d/%m/%Y')}).")
            continue
        break

    new_availability = int(book["availability"]) + 1
    if new_availability > int(book["copies"]):
        new_availability = int(book["copies"])
    book["availability"] = str(new_availability)
    save_books(books)

    append_transactions({
        "bookID": bookid,
        "studentID": studentid,
        "date": date_str,
        "type": "2"
    })
    print(f"Book '{book['title']}' successfully returned by {student['firstName']} on {date_str}.")
    print(f"Current availability: {book['availability']}/{book['copies']}")

def _currently_holds_book(transactions:list, bookid:str, studentid:str) -> bool:
    count = 0
    for t in transactions:
        if t["bookID"] == bookid and t["studentID"] == studentid:
            if t["type"] == "1":
                count += 1
            elif t["type"] == "2":
                count = max(0, count - 1)
    return count > 0