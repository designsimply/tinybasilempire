from db import query_db
from db.sql import (
    ADD_LINK,
    ADD_TAG,
    GET_TAG_ID,
    GET_TAG_NAME,
    ADD_TAGMAP,
    DELETE_TAGMAP,
    GET_TAGS_MAPPED_TO_LINK_ID,
)


# TODO: create Link class
def add_link(title, url, description):
    links = query_db(ADD_LINK, params=(title, url, description))
    link = links[0]
    return link


def add_tags(tag_list):
    tag_ids = []
    for tag in tag_list:
        tag_exists = query_db(GET_TAG_ID, params=[tag])
        if len(tag_exists) > 0:
            tag_ids.append(tag_exists[0])
        else:
            tag_inserted = query_db(ADD_TAG, params=[tag])
            tag_ids.append(tag_inserted[0])
    return tag_ids


def db_get_tag_names_mapped_to_link(link_id):
    tag_list = query_db(GET_TAGS_MAPPED_TO_LINK_ID, params=[link_id])
    tag_names = []
    for tag in tag_list:
        tag_names.append(tag.name)
    return tag_names


def db_get_tag_ids_mapped_to_link(link_id):
    tag_list = query_db(GET_TAGS_MAPPED_TO_LINK_ID, params=[link_id])
    tag_ids = []
    for tag in tag_list:
        tag_ids.append(tag.tag_id)
    return tag_ids


def db_convert_tag_ids_to_names(tag_ids):
    tag_names = []
    for tag_id in tag_ids:
        tag_names_from_db = query_db(GET_TAG_NAME, params=[tag_id])
        tag_names.extend(tag_names_from_db)
    return tag_names


def db_convert_tag_names_to_ids(tag_names):
    tag_ids = []
    for tag_name in tag_names:
        tag_ids_from_db = query_db(GET_TAG_ID, params=[tag_name])
        tag_ids.extend(tag_ids_from_db)
    return tag_ids


def tag_string_to_list(tags):
    if tags == "":
        return []
    else:
        tag_names = tags.split(",")
        tag_list = [tag.strip() for tag in tag_names]
        return tag_list


def tag_list_to_string(tags):
    if len(tags) == 0:
        return ""
    else:
        tag_names = ", ".join(tags)
        return tag_names


def map_tags(link_id, tag_ids):
    tagmap_ids = []
    for tag_id in tag_ids:
        tagmap = query_db(ADD_TAGMAP, params=[link_id, tag_id])
        tagmap_ids.append(tagmap[0])
    tag_names_from_db = []
    tag_names_from_db = db_get_tag_names_mapped_to_link(link_id)
    return tag_names_from_db


def unmap_tags(link_id, tag_ids):
    tag_names_to_remove = []
    tag_names_to_remove = db_convert_tag_ids_to_names(tag_ids)
    tagmap_ids = []
    for tag_id in tag_ids:
        tagmap = query_db(DELETE_TAGMAP, params=[link_id, tag_id])
        tagmap_ids.append(tagmap[0])
    return tag_names_to_remove


def add_new_link(title, url, description, tag_list):
    link = add_link(title, url, description)

    if len(tag_list) > 0:
        tag_ids = add_tags(tag_list)
        tag_list = map_tags(link.id, tag_ids)
    else:
        tag_list = []

    return link, tag_list
