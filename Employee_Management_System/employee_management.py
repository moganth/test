import json
from employee import Employee


# noinspection PyTypeChecker
class EmployeeManagement:
    def __init__(self, json_data):
        self.employees={}
        self.load_employees(json_data)


    def get_employee_by_id(self, emp_id):
        try:
            if emp_id not in self.employees:
                raise ValueError("Employee ID not found !")
            return self.employees[emp_id].display_info()
        except ValueError as e:
            return f"Error: {e}"

    def get_employee_by_name(self, name):
        try:
            found_employees = [
                emp.display_info() for emp in self.employees.values() if emp.name.lower() == name.lower()
            ]
            if found_employees:
                return "\n".join(found_employees)
            else:
                raise ValueError("Employee Name not found!")
        except ValueError as e:
            return f"Error: {e}"

    def add_employee(self, emp_id, name, dept):
        try:
            if emp_id in self.employees:
                raise ValueError("Employee ID already exists!")
            new_employee = Employee(emp_id, name, dept)
            self.employees[emp_id] = new_employee
            return f"Employee {name} added successfully."
        except ValueError as e:
            return f"Error: {e}"


    def save_employees(self, filename="employee.json"):
        try:
            with open(filename, "w") as file:
                employees_data = [{
                    "emp_id": emp.emp_id,
                    "name": emp.name,
                    "dept": emp.dept
                } for emp in self.employees.values()]
                json.dump(employees_data, file, indent=4)
        except Exception as e:
            return f"Error saving data: {e}"

    def load_employees(self,json_data):
        try:
            employees=json.load(json_data)
            for emp in employees:
                self.employees[emp["emp_id"]] = Employee(emp["emp_id"], emp["name"], emp["dept"])
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading json:{e}")
