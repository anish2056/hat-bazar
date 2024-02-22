import logging
from tkinter import EXCEPTION
from requests import JSONDecodeError
from django.core.exceptions import ObjectDoesNotExist
from . import globalparamers

logger = logging.getLogger('django')

def custom_exception(request, e):
    try:
        if isinstance(e, JSONDecodeError):
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.JSON_DECODER_ERROE,
            }
            return message
        if isinstance(e, ValueError):
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.VALUE_ERROR,
            }
            return message
        if isinstance(e, ObjectDoesNotExist):
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.OBJECT_DOES_NOT_EXIST,
            }
            return message
        if isinstance(e, Exception):
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.INTERNAL_ERROR,
            }
            return message
    except Exception as e:
        logger.error(str(e), exc_info=True)
        message = {
            globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
            globalparamers.RESULT_DESCRIPTION: globalparamers.INTERNAL_ERROR,
        }
        return message
