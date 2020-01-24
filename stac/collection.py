from .catalog import Catalog
from .item import ItemCollection
from .utils import Utils

class Extent(dict):
    """The Extent object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Extent metadata.
        """
        super(Extent, self).__init__(data or {})

    @property
    def spatial(self):
        """:return: the spatial extent."""
        return SpatialExtent(self['spatial'])

    @property
    def temporal(self):
        """:return: the temporal extent."""
        return TemporalExtent(self['temporal'])

class SpatialExtent(dict):
    """The Spatial Extent object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Spatial Extent metadata.
        """
        super(SpatialExtent, self).__init__(data or {})

    @property
    def bbox(self):
        """:return: the bbox of the Spatial Extent."""
        return self['bbox']

class TemporalExtent(dict):
    """The Temporal Extent object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Temporal Extent metadata.
        """
        super(TemporalExtent, self).__init__(data or {})

    @property
    def interval(self):
        """:return: the interval of the Temporal Extent."""
        return self['interval']


class Provider(dict):
    """The Provider Object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Provider metadata.
        """
        super(Provider, self).__init__(data or {})

    @property
    def name(self):
        """:return: the Provider name."""
        return self['name']

    @property
    def description(self):
        """:return: the Provider description."""
        return self['description']

    @property
    def roles(self):
        """:return: the Provider roles."""
        return self['description']

    @property
    def url(self):
        """:return: the Provider url."""
        return self['url']


class Collection(Catalog):
    """The STAC Collection."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with collection metadata.
        """
        super(Collection, self).__init__(data or {})

    @property
    def keywords(self):
        """:return: the Collection list of keywords."""
        return self['keywords']

    @property
    def version(self):
        """:return: the Collection version."""
        return self['version']

    @property
    def license(self):
        """:return: the Collection license."""
        return self['license']

    @property
    def providers(self):
        """:return: the Collection list of providers."""
        return [Provider(provider) for provider in self['providers']]

    @property
    def extent(self):
        """:return: the Collection extent."""
        return Extent(self['extent'])

    @property
    def properties(self):
        """:return: the Collection properties."""
        return self['properties']

    def get_items(self, item_id=None, filter=None):
        """:return: A GeoJSON FeatureCollection of STAC Items from the collection."""
        for link in self['links']:
            if link['rel'] == 'items':
                if item_id is not None:
                    data = Utils.get(f'{link["href"]}/{item_id}')
                    return Item(data)
                data = Utils._get(link['href'], params=filter)
                return ItemCollection(data)
        return ItemCollection({})