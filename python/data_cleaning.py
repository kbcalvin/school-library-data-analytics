import pandas as pd
from pathlib import Path


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

# ==========================================================
# 8. DATA QUALITY VALIDATION
# ==========================================================

print("\n" + "=" * 50)
print("DATA QUALITY VALIDATION")
print("=" * 50)

issues = []

# Check duplicate primary keys
for df, key, table_name in [
    (books, "book_id", "Books"),
    (users, "user_id", "Users"),
    (borrowings, "borrowing_id", "Borrowings")
]:
    duplicates = df[key].duplicated().sum()

    if duplicates > 0:
        issues.append(
            f"{table_name}: {duplicates} duplicate IDs found"
        )

# Check invalid book references
invalid_books = ~borrowings["book_id"].isin(books["book_id"])

if invalid_books.any():
    issues.append(
        f"{invalid_books.sum()} borrowings reference unknown books"
    )

# Check invalid user references
invalid_users = ~borrowings["user_id"].isin(users["user_id"])

if invalid_users.any():
    issues.append(
        f"{invalid_users.sum()} borrowings reference unknown users"
    )

# Check invalid borrowing dates
invalid_due_dates = (
    borrowings["due_date"] < borrowings["borrow_date"]
)

if invalid_due_dates.any():
    issues.append(
        f"{invalid_due_dates.sum()} due dates precede borrowing dates"
    )

invalid_return_dates = (
    borrowings["date_returned"] < borrowings["borrow_date"]
)

if invalid_return_dates.any():
    issues.append(
        f"{invalid_return_dates.sum()} return dates precede borrowing dates"
    )

# Check invalid inventory quantities
invalid_inventory = (
    (books["quantity"] < 0) |
    (books["available"] < 0) |
    (books["available"] > books["quantity"])
)

if invalid_inventory.any():
    issues.append(
        f"{invalid_inventory.sum()} books have invalid inventory values"
    )

# Display validation results
if issues:
    print("\nDATA QUALITY ISSUES FOUND:")

    for issue in issues:
        print(f"- {issue}")
else:
    print("\nAll data quality validation checks passed.")

    # ==========================================================
# 9. EXPORT VALIDATED DATASETS
# ==========================================================

if not issues:
    output_dir = Path("data/cleaned")
    output_dir.mkdir(parents=True, exist_ok=True)

    books.to_csv(output_dir / "books_cleaned.csv", index=False)
    users.to_csv(output_dir / "users_cleaned.csv", index=False)
    borrowings.to_csv(
        output_dir / "borrowings_cleaned.csv",
        index=False
    )

    print("\nCleaned datasets exported successfully.")
    print("Location: data/cleaned/")
else:
    print("\nExport cancelled due to data quality issues.")