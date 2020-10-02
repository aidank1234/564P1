-- Find the number of sellers whose rating is higher than 1000.
WITH sellerID AS (
    SELECT DISTINCT Seller FROM Item 
),
sellers AS (
    SELECT UserID, Rating FROM User WHERE EXISTS (SELECT Seller FROM sellerID WHERE Seller = UserID)
)
SELECT COUNT(*) FROM sellers WHERE Rating > 1000;