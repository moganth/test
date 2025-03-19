from file_convertor import FileConvertor

def validate_format(format_chk):
    valid_formats = ["json", "xml", "yaml"]
    if format_chk not in valid_formats:
        raise ValueError("Invalid format. Supported formats are json, xml, and yaml.")

if __name__ == "__main__":
    try:
        input_file = input("1. Enter input file name: ")
        output_file = input("2. Enter output file name: ")
        input_format = input("3. Enter input format (json/xml/yaml): ").lower()
        output_format = input("4. Enter output format (json/xml/yaml): ").lower()

        validate_format(input_format)
        validate_format(output_format)

        converter = FileConvertor(input_file, output_file, input_format, output_format)
        converter.convert()
        print("Conversion completed successfully!")

    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")