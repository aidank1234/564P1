-- Find the number of users who are both sellers and bidders.
WITH sellerID AS (
    SELECT DISTINCT Seller FROM Item 
),
buyerID AS (
    SELECT DISTINCT UserID FROM Bid
),
sellers AS (
    SELECT UserID FROM User WHERE EXISTS (SELECT Seller FROM sellerID WHERE Seller = UserID)
),
buyers AS (
    SELECT UserID AS Buyer FROM User WHERE EXISTS (SELECT UserID FROM buyerID WHERE Buyer = UserID)
)
SELECT COUNT(*) FROM sellers, buyers WHERE sellers.UserID = buyers.Buyer;