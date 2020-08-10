'''
Tests for helpers in the `tasks` Django web application
'''


import datetime
import os
import shutil

from django.conf import settings
from django.test import TestCase

from tasks import helpers


class CheckDailyPackageExistsTests(TestCase):
    '''
    TestCase class for the `check_daily_package_exists` method
    '''

    def test_method_returns_none_if_package_doesnt_exist(self):
        '''
        `check_daily_package_exists` method should return None if a daily package file for the
        input date does not exist on the ftp server
        '''

        # Create a date in the future
        future_date = datetime.datetime(2119, 9, 18).date()

        self.assertIsNone(helpers.check_daily_package_exists(future_date))

    def test_method_returns_filenam_if_package_does_exist(self):
        '''
        `check_daily_package_exists` method should return the correct filename if a daily package
        file for the input date does exist on the ftp server
        '''

        # Create a date in the past
        past_date = datetime.datetime(2019, 9, 17).date()

        self.assertEqual(helpers.check_daily_package_exists(past_date), '20190917_2019179.tar.gz')


class RetrieveDailyPackageFileTests(TestCase):
    '''
    TestCase class for the `retrieve_daily_package_file` method
    '''

    def setUp(self):
        '''
        Common setup across the tests
        '''

        self.valid_file_name = '20190913_2019177.tar.gz'
        self.expected_file_path = os.path.join(settings.TEMP_FILES_DIR, self.valid_file_name)

    def test_method_returns_error_string_if_retrieve_fails(self):
        '''
        `retrieve_daily_package_file` method should return an error string if for whatever reason
        the retrival fails

        Supplied filename is a garbage filename that does not exist on the ftp server, so method
        should return an error string
        '''

        file_name = '20190917_asdasdasd.tar.gz'

        return_str = helpers.retrieve_daily_package_file(file_name)

        self.assertEqual(return_str, '550 ' + file_name + ': No such file or directory')

    def test_method_retrieves_valid_file_and_saves_to_temp_location(self):
        '''
        `retrieve_daily_package_file` method should retrieve a file and save to
        `settings.TEMP_FILES_DIR` if it exists on the ftp

        Supplied filename is a valid file on the ftp server
        '''

        helpers.retrieve_daily_package_file(self.valid_file_name)

        self.assertTrue(os.path.isfile(self.expected_file_path))

        # Delete the file as we are now finished with it
        os.remove(self.expected_file_path)

    def test_method_retrieves_valid_file_and_returns_success_string(self):
        '''
        `retrieve_daily_package_file` method should retrieve a valid file and return a success
        string

        Supplied filename is a valid file on the ftp server
        '''

        return_str = helpers.retrieve_daily_package_file(self.valid_file_name)

        self.assertEqual(return_str, '226 Transfer complete')

        # Delete the file as we are now finished with it
        os.remove(self.expected_file_path)


def copy_files():
    '''
    Copy some files from `TEST_FILES_DIR` to `TEMP_FILES_DIR`
    '''

    files = ['2017-OJS184-376771.xml', '2019-OJS138-339466.xml']

    for file_name in files:
        shutil.copyfile(
            os.path.join(settings.TEST_FILES_DIR, file_name),
            os.path.join(settings.TEMP_FILES_DIR, file_name)
        )


class ClearTempFilesDirTests(TestCase):
    '''
    TestCase class for the `clear_temp_files_dir` helper method
    '''

    def test_temp_files_dir_is_empty_by_default(self):
        '''
        `TEMP_FILES_DIR` should be empty by default for these tests
        '''

        # Check that `TEMP_FILES_DIR` is actually empty
        self.assertFalse(os.listdir(settings.TEMP_FILES_DIR))

    def test_method_doesnt_error_if_temp_files_dir_empty(self):
        '''
        `clear_temp_files_dir` helper method should not error if the `TEMP_FILES_DIR` is empty
        before any delete has taken place
        '''

        # Previous test confirms `TEMP_FILES_DIR` is empty
        self.assertTrue(helpers.clear_temp_files_dir())

    def test_copy_files_check_dir_not_empty(self):
        '''
        `copy_files` method should copy some files to the `TEMP_FILES_DIR` folder
        '''

        # Copy some files to the `TEMP_FILES_DIR`
        copy_files()

        # Confirm listdir returns something, indicating directory contains something
        self.assertTrue(os.listdir(settings.TEMP_FILES_DIR))

    def test_method_deletes_files_and_folders(self):
        '''
        `clear_temp_files_dir` helper method should delete files and folders from `TEMP_FILES_DIR`
        and return True
        '''

        # Copy some files to the `TEMP_FILES_DIR`
        copy_files()

        # Delete the files
        self.assertTrue(helpers.clear_temp_files_dir())

    def test_method_deletes_files_and_folders_check_dir_empty(self):
        '''
        `clear_temp_files_dir` helper method should delete files and folders from `TEMP_FILES_DIR`
        and return True
        '''

        # Copy some files to the `TEMP_FILES_DIR`
        copy_files()

        # Delete the files
        helpers.clear_temp_files_dir()

        # Confirm the folder is empty
        self.assertFalse(os.listdir(settings.TEMP_FILES_DIR))
