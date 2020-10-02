WITH numcategories AS (
    SELECT COUNT(*) AS num, ItemID FROM Category GROUP BY ItemID 
)
SELECT COUNT(*) FROM numcategories WHERE num = 4;