class Employee:
    def __init__(self, emp_id, name, dept):
        self.emp_id = emp_id
        self.name = name
        self.dept = dept

    def display_info(self):
        return f"ID: {self.emp_id}, Name: {self.name}, Dept: {self.dept}"
