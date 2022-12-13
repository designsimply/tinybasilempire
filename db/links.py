from db import query_db
from db.sql import (
    _ADD_LINK,
    _ADD_TAG,
    _GET_TAG_ID,
    _ADD_TAGMAP,
    _GET_TAGNAMES,
)


# TODO: create Link class
def add_link(title, url, description):
    links = query_db(_ADD_LINK, params=(title, url, description))
    link = links[0]
    return link


def add_tags(tag_list):
    tag_ids = []
    for tag in tag_list:
        tag_exists = query_db(_GET_TAG_ID, params=[tag])
        if len(tag_exists) > 0:
            tag_ids.append(tag_exists[0])
        else:
            tag_inserted = query_db(_ADD_TAG, params=[tag])
            tag_ids.append(tag_inserted[0])
    return tag_ids


def map_tags(link_id, tag_ids):
    tag_list = []
    tagmap_ids = []
    for tag_id in tag_ids:
        tagmap = query_db(_ADD_TAGMAP, params=[link_id, tag_id])
        tagmap_ids.append(tagmap[0])
    tag_list = query_db(_GET_TAGNAMES, params=[link_id])
    return tag_list


def add_new_link(title, url, description, tag_list):
    link = add_link(title, url, description)

    if len(tag_list) > 0:
        tag_ids = add_tags(tag_list)
        tag_list = map_tags(link.id, tag_ids)
    else:
        tag_list = []

    return link, tag_list
