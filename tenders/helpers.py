'''
Helper functions for the `tenders` Django app
'''


import datetime
import os
import pytz

import boto3
from botocore.client import Config
from django.conf import settings
from lxml import etree

from tenders import models, xpaths


def check_xml(root, n_s):
    '''
    Method looks through the `root` and performs the following checks:

     * Check the uploaded xml file has the following data:
        * TED_EXPORT_VERSION is in `settings.XML_SCHEMA_VER`
        * NC_CONTRACT_NATURE_CODE is "2" (Supplies)
        * TD_DOCUMENT_TYPE_CODE is "3" (Contract Notice) or "7" (Contract award notice)
        * If Contract Notice:
             * F02_LOT_DIVISION element is present (shows the tender is divided into lots)
             * F02_CPV_CODE.CODE is "33600000" (Pharmaceutical Products)
        * If Contract Award Notice:
             * F03_LOT_DIVISION element is present (shows the tender is divided into lots)
             * F03_CPV_CODE.CODE is "33600000" (Pharmaceutical Products)
        * If the above tests pass, perform the following checks:
        * If Contract Notice:
             * Check the uploaded file contains data we don't already have
                * compare ojs_ref with `ContractNotice` database
        * If Contract Award Notice:
             * Check the uploaded file contains data we don't already have
                * compare ojs_ref with `ContractAwardNotice` database
             * Check the uploaded file has a corresponding `ContractNotice` already
                * compare F03_REF_NOTICE_OJS with `ContractNotice` database

    Returns an `is_valid` boolean and a list of `errors` if any are raised
     * if `is_valid` is True, `errors` will be empty
     * if `is_valid` is False, `errors` will contain one or more error strings
    '''

    # File should have no errors by default
    xml_file_error_list = []

    # Check the xml for the data
    export_version = root.xpath(xpaths.TED_EXPORT_VERSION, namespaces=n_s)

    if export_version not in settings.SUPPORTED_SCHEMAS:
        # Raise error as this file is not in a supported schema
        xml_file_error_list.append('XML schema version is not supported.')

    else:

        contract_nature = root.xpath(xpaths.NC_CONTRACT_NATURE_CODE, namespaces=n_s)
        doc_type_code = root.xpath(xpaths.TD_DOCUMENT_TYPE_CODE, namespaces=n_s)
        ojs_ref = root.xpath(xpaths.NO_DOC_OJS, namespaces=n_s)

        if contract_nature != settings.TARGET_CONTRACT_NATURE_CODE:
            # Raise error as the contract nature is not Supplies
            xml_file_error_list.append(
                'Contract nature is not "' + settings.TARGET_CONTRACT_NATURE_CODE + '".'
            )

        if doc_type_code in settings.SUPPORTED_DOCUMENT_TYPE_CODES:
            # Get the correct model
            tender_model = get_tender_model(root, n_s)

            # Set the correct paths based on the document type
            if doc_type_code == settings.CONTRACT_NOTICE_CODE:
                lot_division_xpath = xpaths.F02_LOT_DIVISION
                cpv_code_xpath = xpaths.F02_CPV_CODE

            elif doc_type_code == settings.CONTRACT_AWARD_NOTICE_CODE:
                lot_division_xpath = xpaths.F03_LOT_DIVISION
                cpv_code_xpath = xpaths.F03_CPV_CODE

            # Check the contract is divided into lots
            if not root.xpath(lot_division_xpath, namespaces=n_s):
                # Raise error
                xml_file_error_list.append(
                    tender_model._meta.verbose_name + ' is not divided into Lots.'
                )

            # Check cpv code
            if root.xpath(cpv_code_xpath, namespaces=n_s) != settings.TARGET_CPV_CODE:
                # Raise error as the CPV code is not Pharmaceutical Products
                xml_file_error_list.append('CPV code is not "' + settings.TARGET_CPV_CODE + '".')

            # If no errors so far, perform additional checks
            if not xml_file_error_list:
                # Check if we already have this data
                if tender_model.objects.filter(ojs_ref=ojs_ref).exists():
                    # Raise error
                    xml_file_error_list.append(
                        tender_model._meta.verbose_name + ' ref "' + ojs_ref +
                        '" already exists in database.'
                    )

                # If contract award notice, check we have a corresponding contract notice
                if doc_type_code == settings.CONTRACT_AWARD_NOTICE_CODE:
                    contract_notice_ojs = root.xpath(xpaths.F03_REF_NOTICE_OJS, namespaces=n_s)

                    # Check if we have this contract notice
                    if not models.ContractNotice.objects \
                        .filter(ojs_ref=contract_notice_ojs).exists():
                        # Raise error
                        xml_file_error_list.append(
                            'Contract Notice ref "' + contract_notice_ojs + '" does not exist ' + \
                            'in database.'
                        )

        else:
            # Raise error
            xml_file_error_list.append('Document type is not supported.')

    return not bool(xml_file_error_list), xml_file_error_list


def create_namespaces_dict(xml_root):
    '''
    Function gets the namespace out of the root and replaces the None default namespace with one
    called 'def'

    The TED export xml contains a default namespace with a None key. This breaks xpath so we need
    to replace it with one with a 'def' key
    '''

    # Grab the namespaces and pop out the default one as this will break xpath
    namespaces = xml_root.nsmap

    default_ns = namespaces.pop(None, None)

    if default_ns:
        # Add to the namespaces with an actual name
        namespaces['def'] = default_ns

    return namespaces


def create_lots(root, n_s, contract_notice):
    '''
    Method creates new `Lot` entries linked to the input `contract_notice` parent from xml data
    defined by `root`

    `root` should be a valid TED tender xml file
    '''

    new_lots = []

    # Create new `Lot` entries with `ContractNotice` parent
    for lot in root.xpath(xpaths.F02_OBJECT_DESCR, namespaces=n_s):

        lot_no = lot.xpath(xpaths.LOT_NO, namespaces=n_s)
        title = lot.xpath(xpaths.LOT_TITLE_P, namespaces=n_s)

        # Check if. If fail, don't create:
        # * the LOT_NO is just a standard integer
        # * the Lot has a title
        if title and lot_no.isdigit():
            # Default data used across all scenarios
            lot_data = {
                'contract_notice': contract_notice,
                'lot_no': lot_no,
                'info_add': '\n'.join(lot.xpath(xpaths.LOT_INFO_ADD_P, namespaces=n_s)),
                'short_descr': '\n'.join(lot.xpath(xpaths.LOT_SHORT_DESCR_P, namespaces=n_s)),
                'title': title
            }

            # Append lot to list ready for bulk_create
            new_lots.append(models.Lot(**lot_data))

    models.Lot.objects.bulk_create(new_lots)


def create_new_tender(root, n_s):
    '''
    Method saves data contained within xml `root` using `n_s` namespace dictionary to new database
    entries based on doc type
     * If doc type is contract notice, save as `ContractNotice` and new `Lots`
     * If doc type is contract award notice, save as `ContractAwardNotice` and update existing
       `Lots`

    Once new entry is created it is returned
    '''

    # Get correct class obj based on document type
    new_entry_class = get_tender_model(root, n_s)

    # Common fields that use the same xpaths across both doc types

    doc_type_code = root.xpath(xpaths.TD_DOCUMENT_TYPE_CODE, namespaces=n_s)

    # Find `Country` entry for foreignkeys
    country = models.Country.objects.get(
        iso_code=root.xpath(xpaths.ISO_COUNTRY_VALUE, namespaces=n_s)
    )

    # Convert datestrings in `datetime.date` objects
    dispatch_date = datetime.datetime.strptime(
        root.xpath(xpaths.DS_DATE_DISPATCH, namespaces=n_s),
        settings.TED_TENDER_DATE_STR
    )

    publication_date = datetime.datetime.strptime(
        root.xpath(xpaths.DATE_PUB, namespaces=n_s),
        settings.TED_TENDER_DATE_STR
    )

    data = {
        'country': country,
        'dispatch_date': dispatch_date,
        'ojs_ref': root.xpath(xpaths.NO_DOC_OJS, namespaces=n_s),
        'publication_date': publication_date,
        'url': root.xpath(xpaths.URI_DOC, namespaces=n_s)
    }

    if doc_type_code == settings.CONTRACT_AWARD_NOTICE_CODE:
        # Find the corresponding contract notice for foreign key
        contract_notice = models.ContractNotice.objects.get(
            ojs_ref=root.xpath(xpaths.F03_REF_NOTICE_OJS, namespaces=n_s)
        )

        value_of_procurement = root.xpath(xpaths.F03_VALUE, namespaces=n_s)

        doc_specific_data = {
            'contract_notice': contract_notice,
            'contracting_body_name': root.xpath(xpaths.F03_OFFICIALNAME, namespaces=n_s),
            'short_descr': root.xpath(xpaths.F03_SHORT_DESCR_P, namespaces=n_s),
            'title': root.xpath(xpaths.F03_TITLE_P, namespaces=n_s)
        }

        # Only add currency and value if value is valid
        if value_of_procurement:
            doc_specific_data['currency'] = models.Currency.objects.get(
                iso_code=root.xpath(xpaths.F03_VALUE_CURRENCY, namespaces=n_s)
            )
            doc_specific_data['value_of_procurement'] = value_of_procurement

    elif doc_type_code == settings.CONTRACT_NOTICE_CODE:

        doc_specific_data = {
            'contracting_body_name': root.xpath(xpaths.F02_OFFICIALNAME, namespaces=n_s),
            'closing_date': get_tender_closing_datetime(root, n_s),
            'full_docs_available': root.xpath(xpaths.F02_DOCUMENT_FULL, namespaces=n_s),
            'procurement_ref': root.xpath(xpaths.F02_REFERENCE_NUMBER, namespaces=n_s),
            'procurement_docs_url': root.xpath(xpaths.F02_URL_DOCUMENT, namespaces=n_s),
            'short_descr': root.xpath(xpaths.F02_SHORT_DESCR_P, namespaces=n_s),
            'title': root.xpath(xpaths.F02_TITLE_P, namespaces=n_s)
        }

    # Add the doc specific fields to the data and create the new entry
    data.update(doc_specific_data)

    new_entry = new_entry_class(**data)
    new_entry.save()

    if doc_type_code == settings.CONTRACT_NOTICE_CODE:
        # Create lots linked to parent `ContractNotice`
        create_lots(root, n_s, new_entry)

    elif doc_type_code == settings.CONTRACT_AWARD_NOTICE_CODE:
        # Update lots linked to related `ContractNotice` using ref contained in
        # `ContractAwardNotice`
        update_lots(root, n_s, new_entry)

    return new_entry


def delete_temporary_file(filepath):
    '''
    Method deletes a file from the `filepath` if it exists
    '''

    if filepath:
        if os.path.exists(filepath):
            # Delete the temp file as we're done with it
            os.remove(filepath)


def get_tender_closing_datetime(root, n_s):
    '''
    Returns a datetime object for the closing date and time for tender submissions
    '''

    date_receipt = root.xpath(xpaths.F02_DATE_RECEIPT_TENDERS, namespaces=n_s)
    time_receipt = root.xpath(xpaths.F02_TIME_RECEIPT_TENDERS, namespaces=n_s)

    if date_receipt:
        # Create datetime base on data available
        if time_receipt:
            date_format = '%Y-%m-%d%H:%M'
            date_str = date_receipt + time_receipt

        else:
            date_format = '%Y-%m-%d'
            date_str = date_receipt

        # Make timezone aware!
        closing_datetime = datetime.datetime.strptime(date_str, date_format) \
            .replace(tzinfo=pytz.timezone('Europe/Brussels'))

    else:
        closing_datetime = None

    return closing_datetime


def get_tender_model(root, n_s):
    '''
    Returns the correct model required to save data contained within the input `root`

     * If `TD_DOCUMENT_TYPE_CODE` is `settings.CONTRACT_AWARD_NOTICE_CODE`, return
       `ContractAwardNotice`
     * If `TD_DOCUMENT_TYPE_CODE` is `settings.CONTRACT_NOTICE_CODE`, return `ContractNotice`
    '''

    doc_type_code = root.xpath(xpaths.TD_DOCUMENT_TYPE_CODE, namespaces=n_s)

    if doc_type_code == settings.CONTRACT_AWARD_NOTICE_CODE:
        return_obj = models.ContractAwardNotice

    elif doc_type_code == settings.CONTRACT_NOTICE_CODE:
        return_obj = models.ContractNotice

    else:
        return_obj = None

    return return_obj


def get_xml_schema():
    '''
    Returns an instance of `lxml.etree.XMLSchema` based on the structure of the `TED_EXPORT.xsd`
    schema file
    '''

    xml_schema_doc = etree.parse(
        os.path.join(settings.BASE_DIR, 'files', 'ted_schema', settings.XML_SCHEMA_VER,
                     settings.XML_SCHEMA_FILE_NAME)
    )

    return etree.XMLSchema(xml_schema_doc)


def get_xml_root(upload_file):
    '''
    Returns the `etree.tree.root` object  and a namespaces dict from a `upload_file` object

    If there is an error, returns `None`
    '''

    try:
        tree = etree.parse(upload_file)
        root = tree.getroot()
        n_s = create_namespaces_dict(root)

    except etree.XMLSyntaxError:
        # Return None if error
        root = None
        n_s = None

    return root, n_s


def new_s3_client():
    '''
    Returns an S3 client instance for use across the `tenders` application

    Used for interacting with files stored on AWS S3. Client obtains credentials by default from
    env variables
    '''

    return boto3.client('s3', config=Config(signature_version='s3v4'))


def update_lots(root, n_s, contract_award_notice):
    '''
    Method updates existing `Lot` entries linked to a referenced `ContractNotice` from contract
    award notice xml data defined by `root`

    `Lot` entries are first created when a `ContractNotice` is created. When a
    `ContractAwardNotice` is published, this contains details of the value of the individual lots.
    So we can update these existing `Lot` entries with value data contained within the
    `ContractAwardNotice` TED tender xml file

    `root` should be a valid F03 TED tender xml file
    '''

    # Grab the xpaths that are specific to the schema of the xml file. We know this file has a
    # valid schema already as `check_xml` has already been called
    schema_xpaths = xpaths.lot_schema_specific_xpaths(
        root.xpath(xpaths.TED_EXPORT_VERSION, namespaces=n_s)
    )

    for lot in contract_award_notice.contract_notice.lot_set.all():

        # Get related xml parts based on lot_no from input `root`
        award_contract = root.xpath('//def:AWARD_CONTRACT[def:LOT_NO={}]'.format(lot.lot_no),
                                    namespaces=n_s)

        # Only update if corresponding data is there
        if award_contract:

            awarded_contract = award_contract[0].xpath(xpaths.F03_LOT_AWARDED_CONTRACT,
                                                       namespaces=n_s)

            # Default data used across all scenarios
            lot.awarded_contract = awarded_contract
            lot.awarded_to_group = award_contract[0].xpath(
                schema_xpaths['F03_LOT_AWARDED_TO_GROUP'], namespaces=n_s
            )

            # Only include extra information if contract actually awarded
            if awarded_contract:
                # Convert datestrings in `datetime.date` objects
                lot.conclusion_date = datetime.datetime.strptime(
                    award_contract[0].xpath(xpaths.F03_LOT_CONCLUSION_DATE, namespaces=n_s),
                    settings.TED_LOT_DATE_STR
                )

                contractor_country = models.Country.objects.get(
                    iso_code=award_contract[0].xpath(schema_xpaths['F03_LOT_CONTRACTOR_COUNTRY'],
                                                     namespaces=n_s)
                )

                lot.contractor_country = contractor_country
                lot.contractor_name = award_contract[0].xpath(
                    schema_xpaths['F03_LOT_CONTRACTOR_NAME'], namespaces=n_s
                )

                val_total = award_contract[0].xpath(schema_xpaths['F03_LOT_VAL_TOTAL'],
                                                    namespaces=n_s)

                # If LOT_VAL_TOTAL is not filled, don't save a value and mark as an estimated value
                if val_total:
                    currency = models.Currency.objects.get(
                        iso_code=award_contract[0].xpath(
                            schema_xpaths['F03_LOT_VAL_TOTAL_CURRENCY'], namespaces=n_s
                        )
                    )

                    lot.currency = currency
                    lot.value = val_total

                else:
                    lot.value_estimated = True

            # Update the lot with this new info
            lot.save()
