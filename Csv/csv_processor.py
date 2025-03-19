import pandas as pd


class CSVProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def read_csv(self):
        try:
            self.data = pd.read_csv(self.file_path, parse_dates=['end'])
            self.data['end'] = self.data['end'].dt.tz_localize(None)
            self.data.columns = [col.replace('_', ' ').title() for col in self.data.columns]

        except FileNotFoundError:
            print("Error: File not found.")
        except Exception as e:
            print(f"Error reading CSV file: {e}")

    def split_by_date(self):
        if self.data is None:
            print("No data available.")
            return {}

        sheets = {}
        for date, df in self.data.groupby(self.data['End'].dt.date):
            sheets[str(date)] = df

        return sheets
