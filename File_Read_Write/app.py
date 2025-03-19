from file_read_util import FileReader
from file_write_util import FileWriter

def main():
    print("Welcome, Choose your operations")

    while True:
        file_name = input("Enter the file name: ")

        operation = input("Do you want to (r)ead or (w)rite or (e)xit a file? ").lower()

        if operation == 'r':
            reader = FileReader(file_name)
            read_msg = reader.file_read()
            print(f"File content: {read_msg}")

        elif operation == 'w':
            writer = FileWriter(file_name)
            data = input("Enter the content to write: ")
            write_msg = writer.file_write(data)
            print(write_msg)

        elif operation == 'e':
            print("Exiting, Visit Again !")
            break

        else:
            print("Invalid operation! choose 'r' or 'w'")

if __name__ =="__main__":
    main()



