class Student:
    def __init__(self, student_name, student_id, fees):
        self.student_name = student_name
        self.student_id = student_id
        self.fees = fees

def add_student_to_file(student, file_path):
    with open(file_path, 'a') as file:
        file.write(f"{student.student_name},{student.student_id},{student.fees}\n")

def read_students_from_file(file_path):
    students = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                student_data = line.strip().split(',')
                if len(student_data) == 3:
                    student = Student(student_data[0], student_data[1], float(student_data[2]))
                    students.append(student)
                else:
                    print(f"Invalid data format in the file: {line}")
    except FileNotFoundError:
        print("Database file not found. Creating a new one.")

    return students

def update_file_with_students(students, file_path):
    with open(file_path, 'w') as file:
        for student in students:
            file.write(f"{student.student_name},{student.student_id},{student.fees}\n")

def add_student(student_list, file_path):
    student_name = input("Enter student name: ")
    student_id = input("Enter student ID: ")
    fees = float(input("Enter fees amount: "))
    
    new_student = Student(student_name, student_id, fees)
    student_list.append(new_student)
    add_student_to_file(new_student, file_path)
    print(f"Student {student_name} added successfully!")

def update_fees(student_list, file_path):
    student_id = input("Enter student ID to update fees: ")
    amount_paid = float(input("Enter the amount paid: "))
    
    found = False
    for student in student_list:
        if student.student_id == student_id:
            student.fees -= amount_paid
            print(f"Fees updated for {student.student_name}. Remaining fees: {student.fees}")
            found = True
            break

    if not found:
        print(f"Student with ID {student_id} not found.")

    update_file_with_students(student_list, file_path)

def display_student_details(student_list):
    student_id = input("Enter student ID to display details: ")
    found = False
    for student in student_list:
        if student.student_id == student_id:
            print(f"Student ID: {student.student_id}")
            print(f"Student Name: {student.student_name}")
            print(f"Fees: {student.fees}")
            found = True
            break
    if not found:
        print(f"Student with ID {student_id} not found.")

def display_due_fees(student_list):
    student_id = input("Enter student ID to display due fees: ")
    found = False
    for student in student_list:
        if student.student_id == student_id:
            print(f"Due Fees for {student.student_name}: {student.fees}")
            found = True
            break
    if not found:
        print(f"Student with ID {student_id} not found.")

# File path for the student database
file_path = "student_database.txt"

# Example usage:
students = read_students_from_file(file_path)

while True:
    print("\n1. Add Student\n2. Update Fees\n3. Display Student Details\n4. Display Due Fees\n5. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        add_student(students, file_path)

    elif choice == '2':
        update_fees(students, file_path)

    elif choice == '3':
        display_student_details(students)

    elif choice == '4':
        display_due_fees(students)

    elif choice == '5':
        break

    else:
        print("Invalid choice. Please enter a valid option.")
