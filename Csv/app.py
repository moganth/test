import pandas as pd
from csv_processor import CSVProcessor
from highlighter import Highlighter

if __name__ == "__main__":
    file_path = "csv_sample.csv"
    output_file = "output.xlsx"

    processor = CSVProcessor(file_path)
    processor.read_csv()
    sheets = processor.split_by_date()

    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        highlighter = Highlighter(writer)

        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            highlighter.apply_formatting(sheet_name, df)

    print(f"Excel file '{output_file}' created successfully.")
