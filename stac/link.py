class Link(dict):
    """Link object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Link metadata.
        """
        super(Link, self).__init__(data or {})

    @property
    def rel(self):
        """:return: the Link relation."""
        return self['rel']

    @property
    def href(self):
        """:return: the Link url."""
        return self['href']

    @property
    def type(self):
        """:return: the type of the Link object."""
        return self['type']

    @property
    def title(self):
        """:return: the title of the Link object."""
        return self['title']
