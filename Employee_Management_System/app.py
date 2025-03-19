
from employee_management import EmployeeManagement

def menu():
    print("\n==> Employee Management System <==")
    print("Choose from the below options: ")
    print("1 => View Employee by ID")
    print("2 => View Employee by Name")
    print("3 => Add New Employee")
    print("4 => Exit")

if __name__ == "__main__":
    try:
        with open("employee.json", "r") as file:
            system = EmployeeManagement(file)
    except FileNotFoundError:
        print("Error: employees.json file not found.")
        exit()

    while True:

        menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            emp_id = int(input("Enter Employee ID: "))
            print(system.get_employee_by_id(emp_id))

        elif choice == "2":
            name = input("Enter Employee Name: ")
            print(system.get_employee_by_name(name))

        elif choice == "3":
            emp_id = int(input("Enter Employee ID: "))
            name = input("Enter Employee Name: ")
            dept = input("Enter Department: ")
            print(system.add_employee(emp_id, name, dept))
            system.save_employees()

        elif choice == "4":
            print("Exiting Employee_Management")
            break

        else:
            print("Invalid Option, Choose from the below options.")