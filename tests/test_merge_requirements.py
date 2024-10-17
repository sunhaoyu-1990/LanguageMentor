import unittest
from unittest.mock import patch, mock_open
from io import StringIO

# Mocking the imported modules/functions from the provided script
from src.utils.merge_requirements import parse_package_spec, get_installed_versions, read_requirements, merge_requirements


class TestPackageManagement(unittest.TestCase):
    
    def test_parse_package_spec(self):
        self.assertEqual(parse_package_spec('package==1.2.3'), ('package', '==', '1.2.3'))
        self.assertEqual(parse_package_spec('package>=2.0.0'), ('package', '>=', '2.0.0'))
        self.assertEqual(parse_package_spec('package'), ('package', None, None))

    @patch('importlib.metadata.version')
    def test_get_installed_versions(self, mock_version):
        mock_version.side_effect = lambda pkg: {'package1': '1.2.3', 'package2': '2.0.0'}[pkg]
        packages = ['package1', 'package2']
        expected = {'package1': '1.2.3', 'package2': '2.0.0'}
        self.assertEqual(get_installed_versions(packages), expected)

    @patch('builtins.open', new_callable=mock_open, read_data='package1==1.2.3\npackage2>=2.0.0\n')
    def test_read_requirements(self, mock_file):
        expected = {
            'package1': '==1.2.3',
            'package2': '>=2.0.0',
        }
        self.assertEqual(read_requirements('requirements.txt'), expected)

    def test_merge_requirements_no_conflict(self):
        installed_versions = {'package1': '1.2.3', 'package2': '2.0.0'}
        req_versions = {'package1': '==1.2.3', 'package2': '>=2.0.0'}
        expected_output = ['package1==1.2.3', 'package2>=2.0.0']
        merged, conflict = merge_requirements(installed_versions, req_versions)
        self.assertEqual(merged, expected_output)
        self.assertFalse(conflict)

    def test_merge_requirements_with_conflict(self):
        installed_versions = {'package1': '1.2.3', 'package2': '2.1.0'}
        req_versions = {'package1': '==1.2.3', 'package2': '==2.0.0'}
        
        expected_output = [
            'package1==1.2.3',
            '<<<<<<< HEAD',
            'package2==2.0.0',
            '=======',
            'package2==2.1.0',
            '>>>>>>> Merged version',
        ]
        
        merged, conflict = merge_requirements(installed_versions, req_versions)
        
        self.assertEqual(merged, expected_output)
        self.assertTrue(conflict)

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.utils.merge_requirements.get_installed_versions')
    @patch('src.utils.merge_requirements.read_requirements')
    @patch('src.utils.merge_requirements.merge_requirements')
    def test_main(self, mock_merge, mock_read, mock_get_installed, mock_file):
        # Mock read_requirements to return some requirements
        mock_read.return_value = {'package1': '==1.2.3'}

        # Mock get_installed_versions to return installed versions
        mock_get_installed.return_value = {'package1': '1.2.3'}

        # Mock merge_requirements to return merged result and no conflict
        mock_merge.return_value = (['package1==1.2.3'], False)

        # Simulate the file writing process
        mock_file_open = mock_open()
        with patch('builtins.open', mock_file_open):
            # Execute the main function to trigger all the actions
            from src.utils.merge_requirements import main
            main()

        # Assert if the merged data was written to requirements.txt
        mock_file_open().write.assert_any_call('package1==1.2.3\n')

if __name__ == "__main__":
    unittest.main()
