_QUERY_ALL_LINKS = """
SELECT
    id
    , url
    , title
    , description
    , datecreated
    , NOW() - datecreated AS timesince
FROM sf_links
ORDER BY datecreated DESC
LIMIT %s
OFFSET %s
"""

_QUERY_SEARCH_LINKS = """
SELECT
    id
    , url
    , title
    , description
    , datecreated
    -- , NOW() - datecreated AS timesince
FROM sf_links
WHERE
    title ~* %s
    OR description ~* %s
ORDER BY datecreated DESC
LIMIT %s
OFFSET %s
"""

_SEARCH_FOR_POTENTIAL_DUPES = """
SELECT
    id
    , url
    , title
    , description
    , datecreated
    , NOW() - datecreated AS timesince
FROM sf_links
WHERE
    url LIKE %s
    or url ~* %s
ORDER BY datecreated DESC
LIMIT %s
OFFSET %s
"""

_SEARCH_FOR_EXACT_URL = """
SELECT
    id
    , url
    , title
    , description
    , datecreated
FROM sf_links
WHERE
    url = %s
ORDER BY datecreated DESC
LIMIT 5
OFFSET 0
"""

_ADD_NEW_LINK = """
INSERT INTO sf_links
    (title, url, description)
VALUES
    (%s, %s, %s)
RETURNING id
"""

_ADD_LINK = """
INSERT INTO sf_links
    (title, url, description)
VALUES
    (%s, %s, %s)
RETURNING id, title, url, description
"""

_GET_LINK = """
SELECT
    id, title, url, description, datecreated
FROM
    sf_links
WHERE
    id=%s
"""

_GET_TAG_ID = """
SELECT
    tag_id
FROM
    sf_tag
WHERE
    name=%s
"""

_ADD_TAG = """
INSERT INTO sf_tag
    (name)
VALUES
    (%s)
ON CONFLICT DO NOTHING
RETURNING tag_id
"""

_ADD_TAGMAP = """
INSERT INTO sf_tagmap
    (link_id, tag_id)
VALUES
    (%s, %s)
ON CONFLICT DO NOTHING
RETURNING tagmap_id
"""

_GET_TAGNAMES_SELECT_DISTINCT = """
SELECT
DISTINCT
    sf_tag.name
FROM
    sf_links, sf_tag, sf_tagmap
WHERE
    sf_tagmap.tag_id = sf_tag.tag_id
    AND sf_tagmap.link_id=%s
"""
_GET_TAGNAMES = """
SELECT
    sf_tag.name
FROM
    sf_tag
JOIN
    sf_tagmap
    ON sf_tag.tag_id = sf_tagmap.tag_id
WHERE
    link_id=%s
"""
