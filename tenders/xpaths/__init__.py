'''
imports in `__init__.py` allow us to seperate xpath definitions into different modules, whilst
still allowing us to access them via the `tenders.xpaths` notation elsewhere
'''


from .common_2014 import DATE_PUB
from .common_2014 import DS_DATE_DISPATCH
from .common_2014 import IA_URL_GENERAL
from .common_2014 import ISO_COUNTRY_VALUE
from .common_2014 import NC_CONTRACT_NATURE_CODE
from .common_2014 import NO_DOC_OJS
from .common_2014 import TD_DOCUMENT_TYPE_CODE
from .common_2014 import TED_EXPORT_VERSION
from .common_2014 import URI_DOC

from .common_2014 import LOT_INFO_ADD_P
from .common_2014 import LOT_NO
from .common_2014 import LOT_SHORT_DESCR_P
from .common_2014 import LOT_TITLE_P

from .f02_2014 import F02_CPV_CODE
from .f02_2014 import F02_DATE_RECEIPT_TENDERS
from .f02_2014 import F02_DOCUMENT_FULL
from .f02_2014 import F02_LOT_DIVISION
from .f02_2014 import F02_OBJECT_DESCR
from .f02_2014 import F02_OFFICIALNAME
from .f02_2014 import F02_REFERENCE_NUMBER
from .f02_2014 import F02_SHORT_DESCR_P
from .f02_2014 import F02_TIME_RECEIPT_TENDERS
from .f02_2014 import F02_TITLE_P
from .f02_2014 import F02_URL_DOCUMENT

from .f03_2014 import F03_AWARD_CONTRACT
from .f03_2014 import F03_CPV_CODE
from .f03_2014 import F03_LOT_AWARDED_CONTRACT
from .f03_2014 import F03_LOT_CONCLUSION_DATE
from .f03_2014 import F03_LOT_DIVISION
from .f03_2014 import F03_LOT_VAL_RANGE_CURRENCY
from .f03_2014 import F03_LOT_VAL_RANGE_HIGH
from .f03_2014 import F03_LOT_VAL_RANGE_LOW
from .f03_2014 import F03_OBJECT_DESCR
from .f03_2014 import F03_OFFICIALNAME
from .f03_2014 import F03_REF_NOTICE_OJS
from .f03_2014 import F03_SHORT_DESCR_P
from .f03_2014 import F03_TITLE_P
from .f03_2014 import F03_VALUE
from .f03_2014 import F03_VALUE_CURRENCY

from .f03_2014 import F03_LOT_AWARDED_TO_GROUP_R2_0_9_S02_E01
from .f03_2014 import F03_LOT_CONTRACTOR_COUNTRY_R2_0_9_S02_E01
from .f03_2014 import F03_LOT_CONTRACTOR_NAME_R2_0_9_S02_E01
from .f03_2014 import F03_LOT_VAL_TOTAL_R2_0_9_S02_E01
from .f03_2014 import F03_LOT_VAL_TOTAL_CURRENCY_R2_0_9_S02_E01
from .f03_2014 import F03_LOT_VAL_EST_TOTAL_R2_0_9_S02_E01
from .f03_2014 import F03_LOT_VAL_EST_CURRENCY_R2_0_9_S02_E01

from .f03_2014 import F03_LOT_AWARDED_TO_GROUP_R2_0_9_S03_E01
from .f03_2014 import F03_LOT_CONTRACTOR_COUNTRY_R2_0_9_S03_E01
from .f03_2014 import F03_LOT_CONTRACTOR_NAME_R2_0_9_S03_E01
from .f03_2014 import F03_LOT_VAL_TOTAL_R2_0_9_S03_E01
from .f03_2014 import F03_LOT_VAL_TOTAL_CURRENCY_R2_0_9_S03_E01
from .f03_2014 import F03_LOT_VAL_EST_TOTAL_R2_0_9_S03_E01
from .f03_2014 import F03_LOT_VAL_EST_CURRENCY_R2_0_9_S03_E01

from .f03_2014 import lot_schema_specific_xpaths
