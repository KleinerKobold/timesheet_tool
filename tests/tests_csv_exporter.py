import unittest
import pandas as pd
from unittest import mock
from datetime import datetime, timedelta
from config import config as test_config
from config import config_nodividers as test_config_nodiv
from pandas.testing import assert_frame_equal
from timesheet.csv_exporter import csv_export, round_hours, filter_df, divide


class TestCsvExport(unittest.TestCase):

    def test_round_hours(self):
        self.assertEqual(round_hours(8.3), 8.5)
        self.assertEqual(round_hours(5.7), 5.75)
        # Add more test cases as needed
    
    
    def generate_test_data(self, num_days):
        current_date = datetime.today()
        data = {
            'Datum': [current_date - timedelta(days=i) for i in range(num_days)],
            'Arbeitszeit': [8.0 + i for i in range(num_days)],
            # Add more columns as needed
        }
        df = pd.DataFrame(data)
        return df

    def test_csv_export_with_config(self):
        # Create a mock configuration
        config = test_config
        self.csv_export_with_config(config)
    
    def test_csv_export_with_config_nodiv(self):
        # Create a mock configuration
        config = test_config_nodiv
        self.csv_export_with_config(config)

    def csv_export_with_config(self, tconfig):
        # Create a mock configuration
        config = tconfig

        # Mock the get_config function to return our custom configuration
        with mock.patch('timesheet.csv_exporter.get_config', return_value=config):
            # Create a test DataFrame for exporting
            data = {
                'Projekt': ["kBites", "Tra"],
                'Datum': [datetime(2023, 7, 20), datetime(2023, 7, 21)],
                'Arbeitszeit': [8.3, 5.7],
                # Add more columns as needed
            }
            df = pd.DataFrame(data)

            # Call the csv_export function
            csv_export(df, days_to_export=0)

        # Test that the CSV file is created and its contents are correct
        with open("test_output.csv", "r") as file:
            csv_content = file.read()
            expected_content = "date;element;hours;comment;aktivitätencode\n"\
                "20.07.2023;E-002;8.5;;\n"\
                "21.07.2023;E-001;5.75;;\n"
            self.assertEqual(csv_content, expected_content)

        # Cleanup: Remove the test_output.csv file
        import os
        os.remove("test_output.csv")


class TestDivideFunction(unittest.TestCase):
    def setUp(self):
        data = {
            'Projekt': ["kBites", "Tra"],
            'Datum': [datetime(2023, 7, 20), datetime(2023, 7, 21)],
            'Arbeitszeit': [8.3, 5.7],
        }
        self.df = pd.DataFrame(data)

    def test_divide_function(self):
        searched_project = "kBites"
        new_projects = {
            "ProjektA": 1.5,
            "ProjektB": 2.0,
        }
        result_df = divide(self.df, searched_project, new_projects)

        self.assertEqual(len(result_df), 3)

        # Test, ob die kopierten Zeilen korrekt sind
        for project_name, multiplicator in new_projects.items():
            filtered_df = self.df[self.df['Projekt'] == searched_project]
            copied_df = filtered_df.copy()
            copied_df['Projekt'] = project_name
            copied_df['Arbeitszeit'] = copied_df['Arbeitszeit'] * multiplicator

            for _, row in copied_df.iterrows():
                self.assertTrue((result_df == row).all(axis=1).any())


if __name__ == '__main__':
    unittest.main()
