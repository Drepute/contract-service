class Error:
    def __init__(self, status_code, error_code, message):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message


AUTHENTICATION_FAILED = Error(400, '400', 'Authentication Failed. Password incorrect')
UNAUTHORIZED = Error(401, '401', 'Unauthorized')

BAD_PARAMS = Error(400, '402', 'Bad Parameters')
BODY_NOT_FOUND = Error(400, '403', 'Body not found')
RESOURCE_EXISTS = Error(400, '409', 'Resource already exists')
NOT_FOUND = Error(404, '405', 'Resource not found')

UNKNOWN = Error(500, '501', 'Uknown Error')
DB_ERROR = Error(500, '502', "DB Error")
REQUESTS_ERROR = Error(500, '503', "Couldn't complete request to server. Please try again")
CHAIN_NOT_SUPPORTED = Error(500, '504', "This chain is not supported")