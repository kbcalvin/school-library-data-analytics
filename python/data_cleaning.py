import pandas as pd


# ==========================================================
# 1. LOAD THE DATA
# ==========================================================

books = pd.read_csv("data/books.csv")
users = pd.read_csv("data/users.csv")
borrowings = pd.read_csv("data/borrowings.csv")


# ==========================================================
# 2. CONVERT DATE COLUMNS
# ==========================================================

borrowings["borrow_date"] = pd.to_datetime(borrowings["borrow_date"])
borrowings["due_date"] = pd.to_datetime(borrowings["due_date"])
borrowings["date_returned"] = pd.to_datetime(borrowings["date_returned"])

# ==========================================================
# 2B. CALCULATE BORROWING PERFORMANCE
# ==========================================================

# Calculate the number of days each book was borrowed
borrowings["days_borrowed"] = (
    borrowings["date_returned"] - borrowings["borrow_date"]
).dt.days

# Calculate how many days late each book was returned
borrowings["days_late"] = (
    borrowings["date_returned"] - borrowings["due_date"]
).dt.days

# Prevent negative values for books returned before the due date
borrowings["days_late"] = borrowings["days_late"].clip(lower=0)

# ==========================================================
# 3. DATASET OVERVIEW
# ==========================================================

print("=" * 50)
print("LIBRARY DATASET OVERVIEW")
print("=" * 50)

print("\nNumber of books:", len(books))
print("Number of users:", len(users))
print("Number of borrowings:", len(borrowings))


# ==========================================================
# 4. MISSING VALUES
# ==========================================================

print("\n" + "=" * 50)
print("MISSING VALUES")
print("=" * 50)

print("\nBooks:")
print(books.isnull().sum())

print("\nUsers:")
print(users.isnull().sum())

print("\nBorrowings:")
print(borrowings.isnull().sum())


# ==========================================================
# 5. DUPLICATE RECORDS
# ==========================================================

print("\n" + "=" * 50)
print("DUPLICATE RECORDS")
print("=" * 50)

print("Duplicate books:", books.duplicated().sum())
print("Duplicate users:", users.duplicated().sum())
print("Duplicate borrowings:", borrowings.duplicated().sum())


# ==========================================================
# 6. CLEANED DATA TYPES
# ==========================================================

print("\n" + "=" * 50)
print("CLEANED DATA TYPES")
print("=" * 50)

print("\nBooks:")
print(books.dtypes)

print("\nUsers:")
print(users.dtypes)

print("\nBorrowings:")
print(borrowings.dtypes)


# ==========================================================
# 7. SAMPLE CLEANED BORROWING DATA
# ==========================================================

print("\n" + "=" * 50)
print("CLEANED BORROWING DATA")
print("=" * 50)

print(borrowings[
    [
        "borrowing_id",
        "user_id",
        "book_id",
        "borrow_date",
        "due_date",
        "date_returned",
        "days_borrowed",
        "days_late"
    ]
].head(10))