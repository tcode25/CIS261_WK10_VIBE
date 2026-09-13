#Terrance Champion
#CIS261
#WK10 VIBE Coding

"""Student Grade Calculator

Option chosen: A - list of dictionaries
"""

import os
import sys

try:
    import termios
    import tty
except ImportError:
    termios = None
    tty = None

FILE_NAME = "student_grades.txt"


def calculate_average(test1, test2, test3):
    """Return the average of three test scores rounded to two decimal places."""
    return round((test1 + test2 + test3) / 3, 2)


def determine_grade(average):
    """Return the letter grade for a student average."""
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def format_score(value):
    """Format a score to exactly two decimal places."""
    return f"{float(value):.2f}"


def student_to_record(student):
    """Convert a student dictionary to the required pipe-delimited format."""
    return (
        f"{student['name']}|{student['id']}|{format_score(student['test1'])}|"
        f"{format_score(student['test2'])}|{format_score(student['test3'])}|"
        f"{format_score(student['average'])}|{student['grade']}"
    )


def save_students(students):
    """Save all student records to the student_grades.txt file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for student in students:
                file.write(student_to_record(student) + "\n")
        print(f"Student records saved to {FILE_NAME}.")
    except OSError as exc:
        print(f"Error saving file: {exc}")


def load_students():
    """Load student records from student_grades.txt when the program starts."""
    students = []

    if not os.path.exists(FILE_NAME):
        print(f"No existing {FILE_NAME} file found. Starting with an empty list.")
        return students

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 7:
                    print(f"Warning: Skipping invalid record on line {line_number}.")
                    continue

                name, student_id, test1, test2, test3, average, grade = parts

                try:
                    student = {
                        "name": name,
                        "id": student_id,
                        "test1": float(test1),
                        "test2": float(test2),
                        "test3": float(test3),
                        "average": float(average),
                        "grade": grade,
                    }
                    students.append(student)
                except ValueError:
                    print(f"Warning: Skipping invalid numeric record on line {line_number}.")
    except OSError as exc:
        print(f"Error loading file: {exc}")

    return students


def add_student(students):
    """Prompt the user for student data, calculate values, and add the record."""
    print("\nAdd a New Student")

    name = input("Enter student name: ").strip()
    if not name:
        print("Student name cannot be blank.")
        return

    student_id = input("Enter student ID: ").strip()
    if not student_id:
        print("Student ID cannot be blank.")
        return

    while True:
        try:
            test1 = float(input("Enter Test 1 score: "))
            test2 = float(input("Enter Test 2 score: "))
            test3 = float(input("Enter Test 3 score: "))
            break
        except ValueError:
            print("Invalid score. Please enter numeric values only.")

    average = calculate_average(test1, test2, test3)
    grade = determine_grade(average)

    student = {
        "name": name,
        "id": student_id,
        "test1": test1,
        "test2": test2,
        "test3": test3,
        "average": average,
        "grade": grade,
    }

    students.append(student)
    save_students(students)
    print(f"Student {name} added successfully. Average: {format_score(average)} | Grade: {grade}")


def display_students(students):
    """Display all students in a formatted table."""
    if not students:
        print("No student records available.")
        return

    headers = ["Name", "ID", "Test 1", "Test 2", "Test 3", "Average", "Grade"]
    rows = []

    for student in students:
        rows.append(
            [
                student["name"],
                student["id"],
                format_score(student["test1"]),
                format_score(student["test2"]),
                format_score(student["test3"]),
                format_score(student["average"]),
                student["grade"],
            ]
        )

    widths = [len(str(header)) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))

    def format_row(values):
        return " | ".join(str(value).ljust(widths[index]) for index, value in enumerate(values))

    print("\nStudent Records")
    print(format_row(headers))
    print("-" * (sum(widths) + (len(widths) - 1) * 3))
    for row in rows:
        print(format_row(row))


def class_statistics(students):
    """Display the highest average, lowest average, and class average."""
    if not students:
        print("No student records available to calculate statistics.")
        return

    averages = [student["average"] for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_average = round(sum(averages) / len(averages), 2)

    print("\nClass Statistics")
    print(f"Highest Average: {format_score(highest)}")
    print(f"Lowest Average: {format_score(lowest)}")
    print(f"Class Average: {format_score(class_average)}")


def search_student(students):
    """Search for a student by name using a case-insensitive comparison."""
    query = input("Enter student name to search: ").strip()
    if not query:
        print("Search name cannot be blank.")
        return

    matches = [student for student in students if query.lower() in student["name"].lower()]

    if not matches:
        print(f"No students match '{query}'.")
        return

    print("\nMatching Student Records")
    for student in matches:
        print(
            f"Name: {student['name']}, ID: {student['id']}, "
            f"Test 1: {format_score(student['test1'])}, Test 2: {format_score(student['test2'])}, "
            f"Test 3: {format_score(student['test3'])}, Average: {format_score(student['average'])}, "
            f"Grade: {student['grade']}"
        )


def read_menu_choice():
    """Read a menu choice and support ESC as an exit key."""
    if os.name == "nt":
        import msvcrt

        key = msvcrt.getwch()
        if key == "\x1b":
            return "ESC"
        return key

    if sys.stdin.isatty() and termios is not None and tty is not None:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if key == "\x1b":
            return "ESC"
        return key

    choice = input("Select an option: ").strip()
    if choice.lower() == "esc":
        return "ESC"
    return choice


def display_menu():
    """Display the program menu and return the user's selection."""
    print("\n=== Student Grade Calculator ===")
    print("1. Add Student")
    print("2. Display All Students")
    print("3. Search Student by Name")
    print("4. View Class Statistics")
    print("5. Save Records")
    print("6. Exit")
    print("Press ESC at any menu to exit.")
    return read_menu_choice()


def main():
    """Run the Student Grade Calculator program."""
    students = load_students()

    while True:
        choice = display_menu()

        if choice == "ESC":
            print("Exiting program. Goodbye!")
            save_students(students)
            break

        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            class_statistics(students)
        elif choice == "5":
            save_students(students)
        elif choice == "6":
            print("Exiting program. Goodbye!")
            save_students(students)
            break
        else:
            print("Invalid option. Please choose a valid menu item (1-6) or press ESC.")


if __name__ == "__main__":
    main()

