import unittest
import yaml
import os
import tempfile
from config import config as test_config
from timesheet.configer import get_config 

class TestGetConfig(unittest.TestCase):

    def test_get_config_existing_file(self):
        data = test_config
        temp_file_descriptor, temp_file_path = tempfile.mkstemp()

        with open(temp_file_path, 'w') as f:
            yaml.safe_dump(data, f, default_flow_style=False)
        os.close(temp_file_descriptor)

        # Test the function
        config = get_config(temp_file_path)
        self.assertEqual(config, data)




if __name__ == '__main__':
    unittest.main()
