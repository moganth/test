class Highlighter:
    def __init__(self, writer):
        self.writer = writer

    def apply_formatting(self, sheet_name, df):
        workbook = self.writer.book
        worksheet = self.writer.sheets[sheet_name]

        value_col_idx = df.columns.get_loc('Value')
        excel_col_letter = chr(65 + value_col_idx)

        start_row = 1
        end_row = df.shape[0] + 1
        column_range = f"{excel_col_letter}{start_row}:{excel_col_letter}{end_row}"

        color_rules = [
            ({"criteria": "<=", "value": 50.0}, "#FF9999"),
            ({"criteria": "between", "value": 50.1, "max": 75.0}, "#9999FF"),
            ({"criteria": "between", "value": 75.1, "max": 90.0}, "#FFFF99"),
            ({"criteria": ">", "value": 90.1}, "#99FF99"),
        ]

        for rule, color in color_rules:
            cell_format = workbook.add_format({'bg_color': color})
            format_settings = {'type': 'cell', 'criteria': rule['criteria'], 'value': rule['value'], 'format': cell_format}
            if 'max' in rule:
                format_settings['maximum'] = rule['max']

            worksheet.conditional_format(column_range, format_settings)

        border_format = workbook.add_format({'border': 1})
        worksheet.set_column(f"{excel_col_letter}:{excel_col_letter}", None, border_format)
