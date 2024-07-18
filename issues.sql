-- Issue 1: Typo in Address - "PIace" instead of "Place"
SELECT UserID, Address
FROM usr.users
WHERE Address LIKE '%PIace%';

-- Issue 2: Size in listings == 0
SELECT Size, COUNT(*) AS count
FROM li.listings
GROUP BY Size
ORDER BY Size ASC;

-- Issue 3: CustomerServiceRequests empty phone and email
SELECT ID, UserID, Phone, Email
FROM cs.CustomerServiceRequests;

SELECT Phone, COUNT(*) AS count
FROM cs.CustomerServiceRequests
GROUP BY Phone
HAVING COUNT(*) > 1
ORDER BY count DESC;

-- Future Possible Issue: No user from SellerID
-- Check if all Items.SellerID has their associated users
SELECT i.SellerID, u.FirstName
FROM im.Items i
LEFT JOIN usr.users u ON i.SellerID = u.UserID
WHERE u.UserID IS NULL;