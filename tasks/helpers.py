'''
Helper functions for the `tasks` Django app
'''


import ftplib
import os
import shutil
import tarfile

from django.conf import settings

from tasks.models import DailyPackageDownloadStatus
from tenders import helpers, models
from tenders.xpaths import TD_DOCUMENT_TYPE_CODE


def bulk_tender_create(status_entry):
    '''
    Method to create new `tenders` and `lots` from file defined by `status_entry.file_name`. Input
    `status_entry` is a `DailyPackageDownloadStatus` entry used to log progress and record errors
    when method is called from a celery task

     * Grabs file from FTP server
     * Extracts to a temp location
     * Loops through each file and creates new `tenders` and `lots` if file contains data we are
       interested in
    '''

    extract_dir = None

    # Make sure the required temp folder exists
    if not os.path.exists(settings.TEMP_FILES_DIR):
        os.mkdir(settings.TEMP_FILES_DIR)

    # if uploaded file exists, try and grab this from S3
    upload_file_path = os.path.join(settings.TEMP_FILES_DIR, status_entry.file_name)

    status_entry.set_status(DailyPackageDownloadStatus.DOWNLOADING)

    # Use ftp to retrieve file to temp location
    return_str = retrieve_daily_package_file(status_entry.file_name)

    # Record if error. Success is code 226, otherwise error
    if not return_str.startswith('226'):
        status_entry.set_status(DailyPackageDownloadStatus.ERROR, return_str)

    # Extract the file if status is not an error
    if not status_entry.is_error():

        status_entry.set_status(DailyPackageDownloadStatus.PROCESSING)

        if tarfile.is_tarfile(upload_file_path):
            # If valid, extract the files to a new directory defined by the archive
            tar = tarfile.open(upload_file_path)

            # Check whether the first member in archive is a directory. If it is, extract
            if tar.getmembers():
                if tar.getmembers()[0].isdir():
                    tar.extractall(settings.TEMP_FILES_DIR)

                    # Save this location for later
                    extract_dir = os.path.join(settings.TEMP_FILES_DIR, tar.getnames()[0])

            # Whatever happens, close the file
            tar.close()

        if not extract_dir:
            # File has not extracted properly, not a tar archive so raise error
            status_entry.set_status(
                DailyPackageDownloadStatus.ERROR,
                'Uploaded .tar.gz archive file is not a valid TED bulk download.'
            )

    # Process the files if status is not an error
    if not status_entry.is_error():

        contract_award_notice_ids = []
        contract_notice_ids = []

        # Loop through all files in `extract_dir`
        for file in os.listdir(extract_dir):

            root, n_s = helpers.get_xml_root(os.path.join(extract_dir, file))

            is_valid, _ = helpers.check_xml(root, n_s)

            if is_valid:
                # Create new `ContractNotice` or `ContractAwardNotice` entry and lots using task
                new_tender = helpers.create_new_tender(root, n_s)

                doc_type_code = root.xpath(TD_DOCUMENT_TYPE_CODE, namespaces=n_s)

                if doc_type_code == settings.CONTRACT_AWARD_NOTICE_CODE:
                    contract_award_notice_ids.append(new_tender.id)

                elif doc_type_code == settings.CONTRACT_NOTICE_CODE:
                    contract_notice_ids.append(new_tender.id)

        # Return a queryset of the new `ContractNotice` and `ContractAwardNotice` entries
        contract_award_notice_qs = models.ContractAwardNotice.objects.filter(
            id__in=contract_award_notice_ids
        )
        contract_notice_qs = models.ContractNotice.objects.filter(id__in=contract_notice_ids)

        if contract_award_notice_qs.exists() or contract_notice_qs.exists():
            msg_str = str(contract_award_notice_qs.count()) +  ' new Contract Award Notice(s) ' + \
                      'and ' + str(contract_notice_qs.count()) + ' new Contract Notice(s) ' + \
                      'added to the database successfully.'

        else:
            msg_str = 'Uploaded file processed successfully but no valid Contract Award ' + \
                      'Notice data was found.'

        status_entry.set_status(DailyPackageDownloadStatus.COMPLETE, msg_str)

    # Delete all the files as we have now finished
    clear_temp_files_dir()


def connect_to_ftp():
    '''
    Method tries to connect to the ftp using credentials supplied in `django.conf.settings`.

     * If successful, return a tuple of (True, `ftplib.FTP` instance)
     * If unsuccessful, return a tuple of (False, None)
    '''

    # Try to connect to host
    try:
        ftp = ftplib.FTP(settings.TED_FTP_ROOT, user=settings.TED_FTP_USERNAME,
                         passwd=settings.TED_FTP_PASSWORD)
        connection_successful = True

    except ConnectionRefusedError:
        ftp = None
        connection_successful = False

    return (connection_successful, ftp)


def check_daily_package_exists(date):
    '''
    Method checks whether a daily package .tar.gz archive file exists on the TED ftp server for
    the input `date` `datetime.date` object

    If a daily package exists, return the filename otherwise return None
    '''

    # Return None by default
    return_file_name = None

    # Try to connect to host
    connection_successful, ftp = connect_to_ftp()

    # Construct the correct file path and see whether a vaild daily package file is there
    if connection_successful:
        try:
            for file_name, _ in ftp.mlsd(
                    path='daily-packages/{:d}/{:02d}'.format(date.year, date.month)):

                # Check if the file_name is the expected format for the input date. If it is,
                # return it
                if file_name.startswith(date.strftime('%Y%m%d')):
                    return_file_name = file_name
                    break

        except ftplib.all_errors:
            # If error, fail silently and just return None by default
            pass

        ftp.close()

    return return_file_name


def clear_temp_files_dir():
    '''
    Method removes all files and folders in the `TEMP_FILES_DIR`
    '''

    for filename in os.listdir(settings.TEMP_FILES_DIR):
        file_path = os.path.join(settings.TEMP_FILES_DIR, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)

        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    return True


def retrieve_daily_package_file(file_name):
    '''
    Method retrieves a daily package .tar.gz archive file from the TED ftp server and saves it to
    a temporary location. The file retrieved is defined by the input `file_name` string

    `check_daily_package_exists` should be called first to confirm the file exists on the ftp
    server

    Returns a string indicating an error or success
    '''

    destination_file_path = os.path.join(settings.TEMP_FILES_DIR, file_name)

    # Try to connect to host
    connection_successful, ftp = connect_to_ftp()

    # Construct the correct file path and see whether a vaild daily package file is there
    if connection_successful:
        try:
            # Change directory to the correct location defined by the filename
            ftp.cwd('daily-packages/{}/{}'.format(file_name[:4], file_name[4:6]))

            # Retrieve correct file and save to temp location
            return_str = ftp.retrbinary(
                'RETR ' + file_name, open(destination_file_path, 'wb').write
            )

        except ftplib.all_errors as err:
            # If there is an error, an empty file may have been created so clear the
            # `TEMP_FILES_DIR`
            clear_temp_files_dir()

            return_str = str(err)

        ftp.close()

    else:
        # There was an error in the connection so return this
        return_str = 'Could not connect to the ftp.'

    return return_str
