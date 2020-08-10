'''
Defines common xpaths used to grab data out of TED export xml files

Xpaths defined below use a 'def' namespace. The default namespace used by TED is None, but this
breaks `lxml.xpath` so we change the None namespace to 'def' using `helpers.create_namespaces_dict`
'''


DATE_PUB = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:REF_OJS/def:DATE_PUB/text())'

DS_DATE_DISPATCH = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:CODIF_DATA' + \
                   '/def:DS_DATE_DISPATCH/text())'

IA_URL_GENERAL = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:NOTICE_DATA' + \
                 '/def:IA_URL_GENERAL/text())'

ISO_COUNTRY_VALUE = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:NOTICE_DATA' + \
                    '/def:ISO_COUNTRY/@VALUE)'

NC_CONTRACT_NATURE_CODE = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:CODIF_DATA' + \
                          '/def:NC_CONTRACT_NATURE/@CODE)'

NO_DOC_OJS = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:NOTICE_DATA/def:NO_DOC_OJS' + \
             '/text())'

ORIGINAL_CPV_CODE = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:NOTICE_DATA' + \
                    '/def:ORIGINAL_CPV/@CODE)'

TD_DOCUMENT_TYPE_CODE = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:CODIF_DATA' + \
                        '/def:TD_DOCUMENT_TYPE/@CODE)'

TED_EXPORT_VERSION = 'string(/def:TED_EXPORT/@VERSION)'

URI_DOC = 'string(/def:TED_EXPORT/def:CODED_DATA_SECTION/def:NOTICE_DATA/def:URI_LIST' + \
          '/def:URI_DOC/text())'

# Lot xpaths local to `F02_OBJECT_DESCR` or `F03_AWARD_CONTRACT` depending on
# `TD_DOCUMENT_TYPE_CODE`
LOT_NO = 'string(def:LOT_NO/text())'

LOT_TITLE_P = 'string(def:TITLE/def:P/text())'

# Lot xpaths local to `F02_OBJECT_DESCR` or `F03_OBJECT_DESCR` depending on `TD_DOCUMENT_TYPE_CODE`
LOT_INFO_ADD_P = 'def:INFO_ADD/def:P/text()' # Will return a list

LOT_SHORT_DESCR_P = 'def:SHORT_DESCR/def:P/text()' # Will return a list
