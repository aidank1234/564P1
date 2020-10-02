-- Find the number of categories that include at least one item with a bid of more than $100.
WITH highbids AS (
    SELECT ItemID FROM Bid WHERE Amount > 100 GROUP BY ItemID
),
cats AS (
    SELECT DISTINCT Category.Name FROM Category, highbids WHERE highbids.ItemID = Category.ItemID
)
SELECT COUNT(*) FROM cats;
