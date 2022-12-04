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
    title LIKE %s 
    OR description LIKE %s 
ORDER BY datecreated DESC 
LIMIT %s 
OFFSET %s
"""
