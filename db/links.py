from db import query_db
from db.sql import (
    ADD_LINK,
    ADD_TAG,
    GET_TAG_ID,
    GET_TAG_NAME,
    ADD_TAGMAP,
    DELETE_TAGMAP,
    GET_TAGS_MAPPED_TO_LINK_ID,
    UPDATE_LINK_NAMED,
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


def update_link(link_id, title, url, description, tag_names):
    links = query_db(
        UPDATE_LINK_NAMED,
        params={
            "link_id": link_id,
            "title": title,
            "url": url,
            "description": description,
        },
    )
    link = links[0]

    current_tag_names = db_get_tag_names_mapped_to_link(link_id)
    current_tag_set = set(current_tag_names)
    new_tag_names = tag_names = tag_string_to_list(tag_names)
    new_tag_set = set(new_tag_names)
    tag_names_to_add = new_tag_set - current_tag_set
    tag_names_to_remove = current_tag_set - new_tag_set
    tag_ids_to_add = db_convert_tag_names_to_ids(tag_names_to_add)
    tag_ids_to_remove = db_convert_tag_names_to_ids(tag_names_to_remove)

    if len(tag_ids_to_remove) > 0:
        # leave old tags in the tags table for now
        # tag_ids = remove_tags(tag_ids_to_remove)
        tags_unmapped = unmap_tags(link.id, tag_ids_to_remove)
    else:
        tags_unmapped = []

    if len(tag_ids_to_add) > 0:
        tag_ids = add_tags(tag_names_to_add)
        tags_mapped = map_tags(link.id, tag_ids)
    else:
        tags_mapped = []

    return link, tags_mapped, tags_unmapped


def delete_link(link_id):
    # $sfdb->query( "DELETE FROM sf_links WHERE id = $link_id;" );
    # $sfdb->query( "DELETE FROM sf_tagmap WHERE link_id = $link_id;" );
    return f"{link_id}"
