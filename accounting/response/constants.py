"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from enum import Enum


class AccountingError:
    def __init__(self, error_code, msg, description=None):
        self.error_code = error_code
        self.msg = msg
        self.description = description


class ErrorTemplate(Enum):
    UNKNOWN_EXCEPTION = AccountingError("ACC_000", "Unspecified Exception")
    MISSING_FIELDS = AccountingError("ACC_001", "Mandatory Fields Missing")
    ADMIN_LOGIN_ERROR = AccountingError("ACC_002", "Admin Login Required.", "Unauthorised")
    PERMISSION_ERROR = AccountingError("ACC_003", "User doesn't have required permission.", "Permission Denied")
    INTERNAL_SERVER_ERROR = AccountingError("ACC_004", "Some Internal Server Error Occurred.", "Internal Server Error")
    NOT_FOUND = AccountingError("ACC_005", "Not Found", "Required entity could not be found. Please try later.")
    INVALID_JSON = AccountingError("ACC_006", "Invalid JSON", "Invalid JSON")
    METHOD_NOT_ALLOWED = AccountingError("ACC_007", "Method Not Allowed")
    INVALID_REQUEST_BODY = AccountingError("ACC_008", "Invalid request body")
    USER_ALREADY_EXISTS = AccountingError("ACC_008", "User already exists")
