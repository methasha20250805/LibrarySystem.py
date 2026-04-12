from Validations import validate_studentid, validate_firstname
from StoreData import load_students, save_students

def student_manage_menu():
    while True:
        print("Manage Students")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Back to Main menu")

        choice = input("Enter your choice[1-3]: ")
        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            break
        else:
            print("Invalid choice")

def add_student():
    print("Add Student")
    students  = load_students()

    while True:
        studentid = input("Enter Student ID(8 digits): ")
        if not validate_studentid(studentid):
            print("Invalid Student ID. Must be exactly 8 digits.")
            continue
        if any (s["studentID"] == studentid for s in students):
            print("Student ID already exists.")
            continue
        break

    while True:
        firstname = input("Enter First Name: ")
        if not validate_firstname(firstname):
            print("Invalid First Name. Only letters and maximum 10 characters are allowed.")
            continue
        break

    new_student = {
        "studentID": studentid,
        "firstName": firstname,
    }

    students.append(new_student)
    save_students(students)
    print("Student Added Successfully")

def view_all_students():
    print("All Student details")
    students = load_students()

    if not students:
        print("No students found in the system.")
        return

    print(f"{"studentID":<12} {"First Name"}")
    print("-" * 25)
    for s in students:
        print(f"{s['studentID']:<12} {s['firstName']}")
    print(f"Total students: {len(students)}")
