class AbstractTemplateError(ValueError):
    """
    Exception indicating an error in the templating process,
    inherits from :class:`ValueError`.
    """
    def __init__(self, message):
        super(AbstractTemplateError, self).__init__(message)


class AbstractGraphError(ValueError):
    """
    Exception indicating an error in the graph building process,
    inherits from :class:`ValueError`.
    """
    def __init__(self, message):
        super(AbstractGraphError, self).__init__(message)
