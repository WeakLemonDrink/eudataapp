'''
Defines xpaths used to grab data out of F02_2014 (Contract Notice) TED export xml files

Xpaths defined below use a 'def' namespace. The default namespace used by TED is None, but this
breaks `lxml.xpath` so we change the None namespace to 'def' using `helpers.create_namespaces_dict`
'''


F02_CPV_CODE = 'string(/def:TED_EXPORT/def:FORM_SECTION/def:F02_2014/def:OBJECT_CONTRACT' + \
               '/def:CPV_MAIN/def:CPV_CODE/@CODE)'

F02_LOT_DIVISION = 'boolean(/def:TED_EXPORT/def:FORM_SECTION/def:F02_2014/def:OBJECT_CONTRACT' + \
                   '/def:LOT_DIVISION)'

F02_OFFICIALNAME = 'string(/def:TED_EXPORT/def:FORM_SECTION/def:F02_2014/def:CONTRACTING_BODY' + \
                   '/def:ADDRESS_CONTRACTING_BODY/def:OFFICIALNAME/text())'

F02_SHORT_DESCR_P = '/def:TED_EXPORT/def:FORM_SECTION/def:F02_2014/def:OBJECT_CONTRACT' + \
                    '/def:SHORT_DESCR/def:P/text()' # Will return a list

F02_TITLE_P = 'string(/def:TED_EXPORT/def:FORM_SECTION/def:F02_2014/def:OBJECT_CONTRACT' + \
              '/def:TITLE/def:P/text())' # Will return a list

F02_OBJECT_DESCR = '/def:TED_EXPORT/def:FORM_SECTION/def:F02_2014/def:OBJECT_CONTRACT' + \
                   '/def:OBJECT_DESCR'

F02_DOCUMENT_FULL = 'boolean(/def:TED_EXPORT/def:FORM_SECTION/def:F02_2014' + \
                    '/def:CONTRACTING_BODY/def:DOCUMENT_FULL)'

F02_URL_DOCUMENT = 'string(/def:TED_EXPORT/def:FORM_SECTION/def:F02_2014/def:CONTRACTING_BODY' + \
                   '/def:URL_DOCUMENT)'

F02_REFERENCE_NUMBER = 'string(/def:TED_EXPORT/def:FORM_SECTION/def:F02_2014' + \
                       '/def:OBJECT_CONTRACT/def:REFERENCE_NUMBER/text())'

F02_DATE_RECEIPT_TENDERS = 'string(/def:TED_EXPORT/def:FORM_SECTION/def:F02_2014/def:PROCEDURE' + \
                           '/def:DATE_RECEIPT_TENDERS/text())'

F02_TIME_RECEIPT_TENDERS = 'string(/def:TED_EXPORT/def:FORM_SECTION/def:F02_2014/def:PROCEDURE' + \
                           '/def:TIME_RECEIPT_TENDERS/text())'

# Lot xpaths local to `OBJECT_DESCR` above
F02_LOT_DURATION = 'string(def:DURATION/text())'

F02_LOT_DURATION_TYPE = 'string(def:DURATION/@TYPE)'
