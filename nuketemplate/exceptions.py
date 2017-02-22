class AbstractTemplateError(ValueError):
    def __init__(self, message):
        super(AbstractTemplateError, self).__init__(message)


class AbstractGraphError(ValueError):
    def __init__(self, message):
        super(AbstractGraphError, self).__init__(message)
