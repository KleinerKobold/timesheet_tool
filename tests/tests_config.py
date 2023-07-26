import unittest
import yaml
import os
import tempfile

from timesheet.configer import get_config 

class TestGetConfig(unittest.TestCase):

    def test_get_config_existing_file(self):
        data = {
            'colors': [
                {'Tra': '00CCFF'},
                {'Data': 'f2b24b'},
                {'kBites': 'f2b24b'},
                {'Intern': 'f2594b'}
            ],
            'csv': {
                'fileName': 'export.csv',
                'round': True,
                'elements': {
                    'Tra': 'E-001',
                    'kBites': 'E-002',
                    'Ninjas': 'E-003',
                    'Gods': 'E-011',
                    'Samurai': 'E-012'
                },
                'codes': {
                    'KBites': 'Erstellung kBite'
                },
                'dividers': {
                    'divider': {
                        'name': 'Ninjas',
                        'targets': {'Gods': 30, 'Samurai': 70}
                    }
                }
            }
        }
        temp_file_descriptor, temp_file_path = tempfile.mkstemp()

        with open(temp_file_path, 'w') as f:
            yaml.safe_dump(data, f, default_flow_style=False)
        os.close(temp_file_descriptor)

        # Test the function
        config = get_config(temp_file_path)
        self.assertEqual(config, data)




if __name__ == '__main__':
    unittest.main()
