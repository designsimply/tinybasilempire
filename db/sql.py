QUERY_ALL_LINKS = """
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

QUERY_ALL_TAGS = """
SELECT DISTINCT
    name,
    COUNT(sf_tag.name) as count
FROM
    sf_tag, sf_tagmap
WHERE
    sf_tag.name  <> ''
    AND sf_tag.tag_id = sf_tagmap.tag_id
GROUP BY
    sf_tag.name
ORDER BY
    sf_tag.name
    -- count DESC
LIMIT %s
OFFSET %s
"""

QUERY_TAGS_COUNT = """
SELECT
    COUNT (DISTINCT name) as count
FROM
    sf_tag, sf_tagmap
WHERE
    sf_tag.tag_id = sf_tagmap.tag_id
"""

QUERY_GET_TAG_LINKS = """
SELECT
    id
    , url
    , title
    , description
    , datecreated
    , NOW() - datecreated AS timesince
FROM
    sf_tagmap tm
    , sf_links l
    , sf_tag t
WHERE tm.tag_id = t.tag_id
    AND ( t.name = %s )
    AND l.id = tm.link_id
ORDER BY lastmodified DESC
LIMIT %s
OFFSET %s
"""

QUERY_GET_TAG_LINKS_COUNT = """
SELECT
    COUNT (*) as count
FROM
    sf_tagmap tm
    , sf_links l
    , sf_tag t
WHERE tm.tag_id = t.tag_id
    AND ( t.name = %s )
    AND l.id = tm.link_id
"""

QUERY_SEARCH_LINKS = """
SELECT
    id
    , url
    , title
    , description
    , datecreated
    , NOW() - datecreated AS timesince
FROM sf_links
WHERE
    title ~* %s
    OR description ~* %s
ORDER BY datecreated DESC
LIMIT %s
OFFSET %s
"""

QUERY_SEARCH_COUNT = """
SELECT
    COUNT(*) as count
FROM sf_links
WHERE
    title ~* %s
    OR description ~* %s
"""

SEARCH_FOR_POTENTIAL_DUPES = """
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

SEARCH_FOR_EXACT_URL = """
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

ADD_NEW_LINK = """
INSERT INTO sf_links
    (title, url, description)
VALUES
    (%s, %s, %s)
RETURNING id
"""

ADD_LINK = """
INSERT INTO sf_links
    (title, url, description)
VALUES
    (%s, %s, %s)
RETURNING id, title, url, description
"""

UPDATE_LINK = """
UPDATE sf_links
SET
    title=%s, url=%s, description=%s
WHERE
    id = %s
RETURNING id, title, url, description, datecreated
"""

UPDATE_LINK_NAMED = """
UPDATE sf_links
SET
    title=%(title)s
    , url=%(url)s
    , description=%(description)s
    , lastmodified=CURRENT_TIMESTAMP
WHERE
    id = %(link_id)s
RETURNING id, title, url, description, datecreated, lastmodified
"""

GET_LINK = """
SELECT
    id
    , title
    , url
    , description
    , datecreated
    , lastmodified
    , NOW() - datecreated AS timesince
FROM
    sf_links
WHERE
    id=%s
"""

GET_TAG_ID = """
SELECT
    tag_id
FROM
    sf_tag
WHERE
    name=%s
"""

GET_TAG_NAME = """
SELECT
    name
FROM
    sf_tag
WHERE
    tag_id=%s
"""

ADD_TAG = """
INSERT INTO sf_tag
    (name)
VALUES
    (%s)
ON CONFLICT DO NOTHING
RETURNING tag_id
"""

ADD_TAGMAP = """
INSERT INTO sf_tagmap
    (link_id, tag_id)
VALUES
    (%s, %s)
ON CONFLICT DO NOTHING
RETURNING tagmap_id
"""

DELETE_TAGMAP = """
DELETE FROM
    sf_tagmap
WHERE
    link_id = %s
    AND tag_id = %s
RETURNING tagmap_id;
"""

GET_TAGS_MAPPED_TO_LINK_ID = """
SELECT
    sf_tag.tag_id,
    sf_tag.name
FROM
    sf_tag
JOIN
    sf_tagmap
    ON sf_tag.tag_id = sf_tagmap.tag_id
WHERE
    link_id=%s
"""
