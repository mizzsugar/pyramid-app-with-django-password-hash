class Error(Exception):
    pass


class ResourceNotFoundError(Error):
    pass


class InvalidCredentialError(Error):
    pass


class AlreadyRegisteredError(Error):
    pass
