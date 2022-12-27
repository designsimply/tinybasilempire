QUERY_ALL_LINKS = """
SELECT
    id
    , url
    , title
    , description
    , datecreated
    , NOW() - datecreated AS timesince
FROM basil_links
ORDER BY datecreated DESC
LIMIT %s
OFFSET %s
"""

QEURY_LINKS_COUNT = """
SELECT
    COUNT(*) as count
FROM
    basil_links
"""

QUERY_ALL_TAGS = """
SELECT DISTINCT
    name,
    COUNT(basil_tags.name) as count
FROM
    basil_tags, basil_tagmap
WHERE
    basil_tags.name  <> ''
    AND basil_tags.tag_id = basil_tagmap.tag_id
GROUP BY
    basil_tags.name
ORDER BY
    basil_tags.name
    -- count DESC
LIMIT %s
OFFSET %s
"""

QUERY_TAGS_COUNT = """
SELECT
    COUNT (DISTINCT name) as count
FROM
    basil_tags, basil_tagmap
WHERE
    basil_tags.tag_id = basil_tagmap.tag_id
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
    basil_tagmap tm
    , basil_links l
    , basil_tags t
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
    basil_tagmap tm
    , basil_links l
    , basil_tags t
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
FROM basil_links
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
FROM basil_links
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
FROM basil_links
WHERE
    url LIKE %s
    or url ~* %s
ORDER BY datecreated DESC
LIMIT %s
OFFSET %s
"""

SEARCH_FOR_POTENTIAL_DUPES_COUNT = """
SELECT
    COUNT(*) as count
FROM basil_links
WHERE
    url LIKE %s
    or url ~* %s
"""

SEARCH_FOR_EXACT_URL = """
SELECT
    id
    , url
    , title
    , description
    , datecreated
FROM basil_links
WHERE
    url = %s
ORDER BY datecreated DESC
LIMIT 5
OFFSET 0
"""

ADD_NEW_LINK = """
INSERT INTO basil_links
    (title, url, description)
VALUES
    (%s, %s, %s)
RETURNING id
"""

ADD_LINK = """
INSERT INTO basil_links
    (title, url, description)
VALUES
    (%s, %s, %s)
RETURNING id, title, url, description
"""

UPDATE_LINK = """
UPDATE basil_links
SET
    title=%s, url=%s, description=%s
WHERE
    id = %s
RETURNING id, title, url, description, datecreated
"""

UPDATE_LINK_NAMED = """
UPDATE basil_links
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
    basil_links
WHERE
    id=%s
"""

GET_TAG_ID = """
SELECT
    tag_id
FROM
    basil_tags
WHERE
    name=%s
"""

GET_TAG_NAME = """
SELECT
    name
FROM
    basil_tags
WHERE
    tag_id=%s
"""

ADD_TAG = """
INSERT INTO basil_tags
    (name)
VALUES
    (%s)
ON CONFLICT DO NOTHING
RETURNING tag_id
"""

ADD_TAGMAP = """
INSERT INTO basil_tagmap
    (link_id, tag_id)
VALUES
    (%s, %s)
ON CONFLICT DO NOTHING
RETURNING tagmap_id
"""

DELETE_TAGMAP = """
DELETE FROM
    basil_tagmap
WHERE
    link_id = %s
    AND tag_id = %s
RETURNING tagmap_id;
"""

GET_TAGS_MAPPED_TO_LINK_ID = """
SELECT
    basil_tags.tag_id,
    basil_tags.name
FROM
    basil_tags
JOIN
    basil_tagmap
    ON basil_tags.tag_id = basil_tagmap.tag_id
WHERE
    link_id=%s
"""

HARD_DELETE_LINK_FROM_TAGMAP = """
DELETE FROM
    basil_tagmap
WHERE
    link_id = %s
"""

HARD_DELETE_LINK = """
DELETE FROM
    basil_links
WHERE
    basil_links.id = %s
RETURNING id
"""
