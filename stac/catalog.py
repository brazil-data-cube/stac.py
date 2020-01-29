from .link import Link

class Catalog(dict):
    """The STAC Catalog."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with catalog metadata.
        """
        super(Catalog, self).__init__(data or {})

    @property
    def stac_version(self):
        """:return: the STAC version."""
        return self['stac_version']

    @property
    def stac_extensions(self):
        """:return: the STAC extensions."""
        return self['stac_extensions']

    @property
    def id(self):
        """:return: the catalog identifier."""
        return self['id']

    @property
    def title(self):
        """:return: the catalog title."""
        return self['title'] if 'title' in self else None

    @property
    def description(self):
        """:return: the catalog description."""
        return self['description']

    @property
    def summaries(self):
        """:return: the catalog summaries."""
        return self['summaries']

    @property
    def links(self):
        """:return: a list of resources in the catalog."""
        return [Link(link) for link in self['links']]
