from ManageBooks import booksmenu
from ManageStudents import student_manage_menu
from IssueBook import issue_book
from ReturnBook import return_book
from TrendGraph import trend_graph
from StoreData import load_books, load_students,load_transactions

def main():
    books = load_books()
    students = load_students()
    transactions = load_transactions()

    print("Library Management System")
    print(f"Loaded: {len(books)} book(s), {len(students)} student(s), "
          f"{len(transactions)} transaction(s).")

    while True:
        print("Main Menu")
        print("1. Manage Books")
        print("2. Manage Students")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Trend Graph")
        print("6. Exit")

        choice = input("Enter your choice(1 - 6): ")

        if choice == "1":
            booksmenu()
        elif choice == "2":
            student_manage_menu()
        elif choice == "3":
            issue_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            trend_graph()
        elif choice == "6":
            print("Thank you for using the Library Management System. Goodbye!")
            break
        else:
            print("Invalid Choice. Please enter a valid choice between 1 and 6.")

        again = input("Do you want to go to the main menu? (yes/no): ")
        if again not in ("yes", "y"):
            print("Thank you for using the Library Management System. Goodbye!")
            break

if __name__ == "__main__":
    main()