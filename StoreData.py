import csv
import os

BOOK_FILE = "book.csv"
STUDENT_FILE = "student.csv"
TRANSACTION_FILE = "transactions.csv"

BOOK_HEADERS = ["bookID", "title", "isbnNumber", "author", "copies", "availability", "price"]
STUDENT_HEADERS = ["studentID", "firstName"]
TRANSACTION_HEADERS = ["bookID", "studentID", "date", "type"]

def _load(filename: str, headers: list):
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            return []
    with open(filename, "r", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def _save(filename: str, headers: list, rows: list):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def load_books():
    return _load(BOOK_FILE, BOOK_HEADERS)
def save_books(books: list):
    _save(BOOK_FILE, BOOK_HEADERS, books)

def load_students():
    return _load(STUDENT_FILE, STUDENT_HEADERS)
def save_students(students: list):
    _save(STUDENT_FILE, STUDENT_HEADERS, students)

def load_transactions():
    return _load(TRANSACTION_FILE, TRANSACTION_HEADERS)
def save_transactions(transactions: list):
    _save(TRANSACTION_FILE, TRANSACTION_HEADERS, transactions)

def append_transactions(transactions: dict):
    file_exists = os.path.isfile(TRANSACTION_FILE)
    with open(TRANSACTION_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TRANSACTION_HEADERS)
        if not file_exists or os.path.getsize(TRANSACTION_FILE) == 0:
            writer.writeheader()
        writer.writerow(transactions)