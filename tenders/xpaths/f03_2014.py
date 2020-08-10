'''
Defines xpaths used to grab data out of F03_2014 (Contract Award Notice) TED export xml files

Xpaths defined below use a 'def' namespace. The default namespace used by TED is None, but this
breaks `lxml.xpath` so we change the None namespace to 'def' using `helpers.create_namespaces_dict`
'''


def lot_schema_specific_xpaths(schema_version):
    '''
    Method returns a dictionary of the correct lot xpaths for the input `schema_version`
    '''

    if schema_version == 'R2.0.9.S02.E01':
        xpath_dict = {
            'F03_LOT_AWARDED_TO_GROUP': F03_LOT_AWARDED_TO_GROUP_R2_0_9_S02_E01,
            'F03_LOT_CONTRACTOR_COUNTRY': F03_LOT_CONTRACTOR_COUNTRY_R2_0_9_S02_E01,
            'F03_LOT_CONTRACTOR_NAME': F03_LOT_CONTRACTOR_NAME_R2_0_9_S02_E01,
            'F03_LOT_VAL_TOTAL': F03_LOT_VAL_TOTAL_R2_0_9_S02_E01,
            'F03_LOT_VAL_TOTAL_CURRENCY': F03_LOT_VAL_TOTAL_CURRENCY_R2_0_9_S02_E01,
            'F03_LOT_VAL_EST_TOTAL': F03_LOT_VAL_EST_TOTAL_R2_0_9_S02_E01,
            'F03_LOT_VAL_EST_CURRENCY': F03_LOT_VAL_EST_CURRENCY_R2_0_9_S02_E01
        }

    elif schema_version == 'R2.0.9.S03.E01':
        xpath_dict = {
            'F03_LOT_AWARDED_TO_GROUP': F03_LOT_AWARDED_TO_GROUP_R2_0_9_S03_E01,
            'F03_LOT_CONTRACTOR_COUNTRY': F03_LOT_CONTRACTOR_COUNTRY_R2_0_9_S03_E01,
            'F03_LOT_CONTRACTOR_NAME': F03_LOT_CONTRACTOR_NAME_R2_0_9_S03_E01,
            'F03_LOT_VAL_TOTAL': F03_LOT_VAL_TOTAL_R2_0_9_S03_E01,
            'F03_LOT_VAL_TOTAL_CURRENCY': F03_LOT_VAL_TOTAL_CURRENCY_R2_0_9_S03_E01,
            'F03_LOT_VAL_EST_TOTAL': F03_LOT_VAL_EST_TOTAL_R2_0_9_S03_E01,
            'F03_LOT_VAL_EST_CURRENCY': F03_LOT_VAL_EST_CURRENCY_R2_0_9_S03_E01
        }

    return xpath_dict


# TENDER xpaths
# See ./files/ted_schema/R2_0_9_S03_E01/F03_2014.xsd


F03_CPV_CODE = 'string(/def:TED_EXPORT/def:FORM_SECTION/def:F03_2014/def:OBJECT_CONTRACT' + \
               '/def:CPV_MAIN/def:CPV_CODE/@CODE)'

# Reference to originating contract notice
F03_REF_NOTICE_OJS = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:NOTICE_DATA' + \
                     '/def:REF_NOTICE/def:NO_DOC_OJS/text())'

F03_VALUE = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:NOTICE_DATA/def:VALUES' + \
            '/def:VALUE/text())'

F03_VALUE_CURRENCY = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:NOTICE_DATA/def:VALUES' + \
                     '/def:VALUE/@CURRENCY)'

F03_LOT_DIVISION = 'boolean(/def:TED_EXPORT/def:FORM_SECTION/def:F03_2014/def:OBJECT_CONTRACT' + \
                   '/def:LOT_DIVISION)'

F03_OFFICIALNAME = 'string(/def:TED_EXPORT/def:FORM_SECTION/def:F03_2014/def:CONTRACTING_BODY' + \
                   '/def:ADDRESS_CONTRACTING_BODY/def:OFFICIALNAME/text())'

F03_SHORT_DESCR_P = '/def:TED_EXPORT/def:FORM_SECTION/def:F03_2014/def:OBJECT_CONTRACT' + \
                    '/def:SHORT_DESCR/def:P/text()' # Will return a list

F03_TITLE_P = 'string(/def:TED_EXPORT/def:FORM_SECTION/def:F03_2014/def:OBJECT_CONTRACT' + \
              '/def:TITLE/def:P/text())' # Will return a list

F03_AWARD_CONTRACT = '/def:TED_EXPORT/def:FORM_SECTION/def:F03_2014/def:AWARD_CONTRACT'

F03_OBJECT_DESCR = '/def:TED_EXPORT/def:FORM_SECTION/def:F03_2014/def:OBJECT_CONTRACT' + \
                   '/def:OBJECT_DESCR'

# Lot xpaths local to `AWARD_CONTRACT` above
F03_LOT_AWARDED_CONTRACT = 'boolean(def:AWARDED_CONTRACT)'

F03_LOT_AWARDED_TO_GROUP_R2_0_9_S02_E01 = 'boolean(def:AWARDED_CONTRACT/def:AWARDED_TO_GROUP)'

F03_LOT_AWARDED_TO_GROUP_R2_0_9_S03_E01 = 'boolean(def:AWARDED_CONTRACT/def:CONTRACTORS' + \
                                          '/def:AWARDED_TO_GROUP)'

F03_LOT_CONCLUSION_DATE = 'string(def:AWARDED_CONTRACT/def:DATE_CONCLUSION_CONTRACT/text())'

F03_LOT_CONTRACTOR_COUNTRY_R2_0_9_S02_E01 = 'string(def:AWARDED_CONTRACT/def:CONTRACTOR' + \
                                        '/def:ADDRESS_CONTRACTOR/def:COUNTRY/@VALUE)'

F03_LOT_CONTRACTOR_COUNTRY_R2_0_9_S03_E01 = 'string(def:AWARDED_CONTRACT/def:CONTRACTORS' + \
                                        '/def:CONTRACTOR/def:ADDRESS_CONTRACTOR/def:COUNTRY' + \
                                        '/@VALUE)'

F03_LOT_CONTRACTOR_NAME_R2_0_9_S02_E01 = 'string(def:AWARDED_CONTRACT/def:CONTRACTOR' + \
                                     '/def:ADDRESS_CONTRACTOR/def:OFFICIALNAME/text())'

F03_LOT_CONTRACTOR_NAME_R2_0_9_S03_E01 = 'string(def:AWARDED_CONTRACT/def:CONTRACTORS' + \
                                     '/def:CONTRACTOR/def:ADDRESS_CONTRACTOR/def:OFFICIALNAME' + \
                                     '/text())'

F03_LOT_NO_AWARDED_TO_GROUP = 'boolean(def:AWARDED_CONTRACT/def:CONTRACTORS' + \
                              '/def:NO_AWARDED_TO_GROUP)'

F03_LOT_VAL_TOTAL_R2_0_9_S02_E01 = 'string(def:AWARDED_CONTRACT/def:VAL_TOTAL/text())'

F03_LOT_VAL_TOTAL_R2_0_9_S03_E01 = 'string(def:AWARDED_CONTRACT/def:VALUES/def:VAL_TOTAL/text())'

F03_LOT_VAL_TOTAL_CURRENCY_R2_0_9_S02_E01 = 'string(def:AWARDED_CONTRACT/def:VAL_TOTAL/@CURRENCY)'

F03_LOT_VAL_TOTAL_CURRENCY_R2_0_9_S03_E01 = 'string(def:AWARDED_CONTRACT/def:VALUES' + \
                                            '/def:VAL_TOTAL/@CURRENCY)'

F03_LOT_VAL_EST_TOTAL_R2_0_9_S02_E01 = 'string(def:AWARDED_CONTRACT/def:VAL_ESTIMATED_TOTAL/text())'

F03_LOT_VAL_EST_TOTAL_R2_0_9_S03_E01 = 'string(def:AWARDED_CONTRACT/def:VALUES' + \
                                   '/def:VAL_ESTIMATED_TOTAL/text())'

F03_LOT_VAL_EST_CURRENCY_R2_0_9_S02_E01 = 'string(def:AWARDED_CONTRACT/def:VAL_ESTIMATED_TOTAL' + \
                                      '/@CURRENCY)'

F03_LOT_VAL_EST_CURRENCY_R2_0_9_S03_E01 = 'string(def:AWARDED_CONTRACT/def:VALUES' + \
                                      '/def:VAL_ESTIMATED_TOTAL/@CURRENCY)'

F03_LOT_VAL_RANGE_CURRENCY = 'string(def:AWARDED_CONTRACT/def:VALUES/def:VAL_RANGE_TOTAL/@CURRENCY)'

F03_LOT_VAL_RANGE_LOW = 'string(def:AWARDED_CONTRACT/def:VALUES/def:VAL_RANGE_TOTAL/def:LOW/text())'

F03_LOT_VAL_RANGE_HIGH = 'string(def:AWARDED_CONTRACT/def:VALUES/def:VAL_RANGE_TOTAL/def:HIGH' + \
                         '/text())'
