import os
import psycopg2
import psycopg2.extras
from db.db import get_db_connection


# TODO: create Link class
def add_new_link(title, url, description, tag_names):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute(
                "INSERT INTO sf_links (title, url, description) VALUES (%s, %s, %s) RETURNING id",
                [title, url, description],
            )
            new_link = cur.fetchone()
            inserted_link_id = new_link.id

        if len(tag_names) > 0:
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
                tag_ids = []
                for tag_name in tag_names:
                    cur.execute(
                        "INSERT INTO sf_tag (name) VALUES (%s) ON CONFLICT DO NOTHING RETURNING tag_id",
                        [tag_name],
                    )
                    inserted_tag = cur.fetchone()
                    tag_ids.append(inserted_tag.tag_id)
                for tag_id in tag_ids:
                    cur.execute(
                        "INSERT INTO sf_tagmap (tag_id, link_id) VALUES (%s, %s) ON CONFLICT DO NOTHING RETURNING tagmap_id",
                        [tag_id, inserted_link_id],
                    )
                cur.execute(
                    "SELECT sf_tag.name FROM sf_tag JOIN sf_tagmap ON sf_tag.tag_id = sf_tagmap.tag_id WHERE link_id=%s",
                    [inserted_link_id],
                )
                new_link_tag_names = cur.fetchall()
        else:
            new_link_tag_names = ""

    return new_link, new_link_tag_names
