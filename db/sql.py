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
    , NOW() - datecreated AS timesince
FROM sf_links 
WHERE 
    title ~* %s 
    OR description ~* %s 
ORDER BY datecreated DESC 
LIMIT %s 
OFFSET %s
"""
