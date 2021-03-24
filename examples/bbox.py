#!/usr/bin/env python
# coding: utf-8

#%%
import stac

#%%
s = stac.STAC('https://brazildatacube.dpi.inpe.br/stac/')

#%%
s.catalog

#%%
collection = s.collection('CB4_64_16D_STK-1')
collection

#%%
items = collection.get_items(
    filter = {
        'bbox':'-56.86523437500001,-15.919073517982413,-53.17382812500001,-13.902075852500483',
        'time':'2016-09-13/2019-12-31'
    }
)
items
