
# Student Record and Academic Management System
# Python Collections: Strings, Lists, Tuples, Sets, Dictionaries
# Records are saved automatically in students.json.

import json
import os

DATA_FILE = "students.json"
students = []


def load_students():
    """Load saved records when the program starts."""
    global students
    if not os.path.exists(DATA_FILE):
        students = []
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        students = data if isinstance(data, list) else []
        print(f"Loaded {len(students)} saved student record(s).")
    except (json.JSONDecodeError, OSError):
        students = []
        print("Could not read saved records. Starting with an empty list.")


def save_students():
    """Save all records to a JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
    except OSError:
        print("Warning: records could not be saved.")


def find_student(roll_no):
    for student in students:
        if student["roll_no"].lower() == roll_no.lower():
            return student
    return None


def read_number(prompt, minimum=None, maximum=None, whole_number=False):
    while True:
        try:
            value = input(prompt).strip()
            number = int(value) if whole_number else float(value)
            if minimum is not None and number < minimum:
                print(f"Value must be at least {minimum}.")
                continue
            if maximum is not None and number > maximum:
                print(f"Value must not be more than {maximum}.")
                continue
            return number
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def read_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def read_marks():
    return read_number("Enter marks (0-100): ", 0, 100)


def read_attendance():
    return read_number("Enter attendance percentage (0-100): ", 0, 100)


def add_student():
    print("\n--- Add Student ---")
    roll_no = read_non_empty("Enter Roll Number: ")
    if find_student(roll_no):
        print("This roll number already exists. Duplicate record not added.")
        return

    name = read_non_empty("Enter Student Name: ")
    department = read_non_empty("Enter Department: ")
    registration_no = input("Enter Registration Number (or press Enter to skip): ").strip()
    dob = input("Enter Date of Birth (or press Enter to skip): ").strip()
    address = input("Enter Address (or press Enter to skip): ").strip()
    email = input("Enter Email ID (or press Enter to skip): ").strip()
    phone = input("Enter Contact Number (or press Enter to skip): ").strip()

    subjects_text = input("Enter Subjects separated by commas: ").strip()
    subjects = [subject.strip() for subject in subjects_text.split(",") if subject.strip()]

    marks = read_marks()
    attendance = read_attendance()

    # Tuple example: roll number and registration number are grouped as identifiers.
    identifiers = (roll_no, registration_no)

    student = {
        "roll_no": identifiers[0],
        "registration_no": identifiers[1],
        "name": name,
        "department": department,
        "dob": dob,
        "address": address,
        "email": email,
        "phone": phone,
        "subjects": subjects,
        "marks": marks,
        "attendance": attendance
    }

    students.append(student)
    save_students()
    print("Student added and saved successfully!")


def print_student(student):
    print("-" * 35)
    print("Roll Number:", student.get("roll_no", ""))
    print("Registration Number:", student.get("registration_no", ""))
    print("Name:", student.get("name", ""))
    print("Department:", student.get("department", ""))
    print("Date of Birth:", student.get("dob", ""))
    print("Address:", student.get("address", ""))
    print("Email:", student.get("email", ""))
    print("Contact:", student.get("phone", ""))
    print("Subjects:", ", ".join(student.get("subjects", [])))
    print("Marks:", student.get("marks", 0))
    print("Attendance:", str(student.get("attendance", 0)) + "%")


def display_students():
    print("\n--- Display All Students ---")
    if not students:
        print("No student records found.")
        return
    for student in students:
        print_student(student)
    print("-" * 35)
    print("Total students:", len(students))


def search_student():
    print("\n--- Search Student ---")
    roll_no = input("Enter Roll Number to search: ").strip()
    student = find_student(roll_no)
    if student:
        print_student(student)
    else:
        print("Student not found.")


def update_student():
    print("\n--- Update Student ---")
    roll_no = input("Enter Roll Number to update: ").strip()
    student = find_student(roll_no)
    if not student:
        print("Student not found.")
        return

    print("Press Enter to keep the existing value.")
    fields = [
        ("name", "Name"),
        ("department", "Department"),
        ("registration_no", "Registration Number"),
        ("dob", "Date of Birth"),
        ("address", "Address"),
        ("email", "Email ID"),
        ("phone", "Contact Number")
    ]
    for key, label in fields:
        current = student.get(key, "")
        value = input(f"{label} [{current}]: ").strip()
        if value:
            student[key] = value

    subjects_text = input(
        "Update subjects (comma-separated, or Enter to keep current): "
    ).strip()
    if subjects_text:
        student["subjects"] = [
            item.strip() for item in subjects_text.split(",") if item.strip()
        ]

    if input("Update marks? (y/n): ").strip().lower() == "y":
        student["marks"] = read_marks()
    if input("Update attendance? (y/n): ").strip().lower() == "y":
        student["attendance"] = read_attendance()

    save_students()
    print("Student record updated and saved.")


def delete_student():
    print("\n--- Delete Student ---")
    roll_no = input("Enter Roll Number to delete: ").strip()
    student = find_student(roll_no)
    if not student:
        print("Student not found.")
        return

    confirm = input(
        f'Confirm deletion of {student.get("name", "this student")}? (y/n): '
    ).strip().lower()
    if confirm == "y":
        students.remove(student)
        save_students()
        print("Student deleted.")
    else:
        print("Deletion cancelled.")


def average_marks():
    print("\n--- Average Marks ---")
    if not students:
        print("No student records found.")
        return
    average = sum(float(s.get("marks", 0)) for s in students) / len(students)
    print(f"Average Marks: {average:.2f}")


def highest_scorer():
    print("\n--- Highest Scorer ---")
    if not students:
        print("No student records found.")
        return
    highest = max(students, key=lambda s: float(s.get("marks", 0)))
    print_student(highest)


def list_by_department():
    print("\n--- List Students by Department ---")
    department = input("Enter Department to list: ").strip()
    matches = [
        student for student in students
        if student.get("department", "").lower() == department.lower()
    ]
    if not matches:
        print("No students found in this department.")
        return
    for student in matches:
        print_student(student)
    print("Students in this department:", len(matches))


def count_students():
    print("\n--- Count Students ---")
    print("Total student records:", len(students))
    if students:
        # Set keeps only unique department names.
        departments = {s.get("department", "") for s in students if s.get("department", "")}
        print("Number of different departments:", len(departments))
        print("Departments:", ", ".join(sorted(departments)))


def collections_demo():
    print("\n--- Python Collections Demonstration ---")
    # List: student records and subject lists.
    print("Student records are stored in a LIST.")
    print("Number of records:", len(students))

    # Tuple: immutable example.
    sample_tuple = ("Roll Number", "Registration Number", "Date of Birth")
    print("Example tuple:", sample_tuple)

    # Set: unique departments and subjects.
    departments = {s.get("department", "") for s in students if s.get("department", "")}
    subjects = {
        subject
        for s in students
        for subject in s.get("subjects", [])
    }
    print("Unique departments (set):", departments)
    print("Unique subjects (set):", subjects)

    # String examples.
    if students:
        name = students[0].get("name", "")
        print("First student's name in uppercase:", name.upper())
        print("First student's name length:", len(name))
    else:
        print("Add a student to see string examples.")


def main():
    load_students()
    while True:
        print("\n==========================================")
        print(" STUDENT RECORD AND ACADEMIC MANAGEMENT")
        print("==========================================")
        print("1. Add Student")
        print("2. Display All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Calculate Average Marks")
        print("7. Find Highest Scorer")
        print("8. List Students by Department")
        print("9. Count Students")
        print("10. Python Collections Demonstration")
        print("11. Exit")

        choice = input("Enter your choice (1-11): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            average_marks()
        elif choice == "7":
            highest_scorer()
        elif choice == "8":
            list_by_department()
        elif choice == "9":
            count_students()
        elif choice == "10":
            collections_demo()
        elif choice == "11":
            save_students()
            print("Records saved. Thank you!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 11.")


if __name__ == "__main__":
    main()
