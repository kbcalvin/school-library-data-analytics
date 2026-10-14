-- ==========================================================
-- SCHOOL LIBRARY DATA ANALYTICS
-- SQL ANALYSIS
-- ==========================================================

-- ==========================================================
-- ANALYSIS 1: MOST BORROWED BOOKS
-- ==========================================================

SELECT
    b.book_id,
    b.name AS book_name,
    COUNT(br.borrowing_id) AS times_borrowed
FROM books b
LEFT JOIN borrowings br
    ON b.book_id = br.book_id
GROUP BY
    b.book_id,
    b.name
ORDER BY
    times_borrowed DESC;

    -- ==========================================================
-- ANALYSIS 2: LOW-UTILISATION BOOKS
-- ==========================================================

SELECT
    b.book_id,
    b.name AS book_name,
    COUNT(br.borrowing_id) AS times_borrowed
FROM books b
LEFT JOIN borrowings br
    ON b.book_id = br.book_id
GROUP BY
    b.book_id,
    b.name
ORDER BY
    times_borrowed ASC;

    -- ==========================================================
-- ANALYSIS 3: MONTHLY BORROWING ACTIVITY
-- ==========================================================

SELECT
    YEAR(borrow_date) AS year,
    MONTH(borrow_date) AS month,
    COUNT(borrowing_id) AS total_borrowings
FROM borrowings
GROUP BY
    YEAR(borrow_date),
    MONTH(borrow_date)
ORDER BY
    year,
    month;

    -- ==========================================================
-- ANALYSIS 4: LATE RETURNS
-- ==========================================================

SELECT
    borrowing_id,
    user_id,
    book_id,
    due_date,
    date_returned,
    DATEDIFF(date_returned, due_date) AS days_late
FROM borrowings
WHERE date_returned > due_date
ORDER BY
    days_late DESC;

    -- ==========================================================
-- ANALYSIS 5: MOST ACTIVE USERS
-- ==========================================================

SELECT
    u.user_id,
    u.name,
    COUNT(br.borrowing_id) AS times_borrowed
FROM users u
LEFT JOIN borrowings br
    ON u.user_id = br.user_id
GROUP BY
    u.user_id,
    u.name
ORDER BY
    times_borrowed DESC;

    -- ==========================================================
-- ANALYSIS 6: PENALTY RATE
-- ==========================================================

SELECT
    COUNT(*) AS total_borrowings,

    SUM(
        CASE
            WHEN date_returned > due_date THEN 1
            ELSE 0
        END
    ) AS penalty_transactions,

    ROUND(
        (
            SUM(
                CASE
                    WHEN date_returned > due_date THEN 1
                    ELSE 0
                END
            ) / COUNT(*)
        ) * 100,
        2
    ) AS penalty_rate_percentage

FROM borrowings;

-- ==========================================================
-- ANALYSIS 7: BOOK DEMAND AND INVENTORY
-- ==========================================================

SELECT
    b.book_id,
    b.name AS book_name,
    COUNT(br.borrowing_id) AS times_borrowed,
    b.quantity,
    b.available,

    ROUND(
        (
            (b.quantity - b.available)
            / b.quantity
        ) * 100,
        2
    ) AS borrowed_copy_percentage

FROM books b

LEFT JOIN borrowings br
    ON b.book_id = br.book_id

GROUP BY
    b.book_id,
    b.name,
    b.quantity,
    b.available

ORDER BY
    times_borrowed DESC;