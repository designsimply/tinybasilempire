import psycopg2
import psycopg2.extras
from db.db import get_db_connection
from db.sql import _ADD_NEW_LINK, _ADD_TAGS, _ADD_TAGMAP, _GET_TAGNAMES_WITH_JOIN


# TODO: create Link class
def add_new_link(title, url, description, tag_names):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute(
                _ADD_NEW_LINK,
                [title, url, description],
            )
            new_link = cur.fetchone()
            inserted_link_id = new_link.id

        if len(tag_names) > 0:
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
                tag_ids = []
                for tag_name in tag_names:
                    cur.execute(
                        _ADD_TAGS,
                        [tag_name],
                    )
                    inserted_tag = cur.fetchone()
                    tag_ids.append(inserted_tag.tag_id)
                for tag_id in tag_ids:
                    cur.execute(
                        _ADD_TAGMAP,
                        [tag_id, inserted_link_id],
                    )
                cur.execute(
                    _GET_TAGNAMES_WITH_JOIN,
                    [inserted_link_id],
                )
                new_link_tag_names = cur.fetchall()
        else:
            new_link_tag_names = ""

    return new_link, new_link_tag_names
