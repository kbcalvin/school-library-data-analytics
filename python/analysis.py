import pandas as pd



# ==========================================================
# LOAD CLEANED AND VALIDATED DATASETS
# ==========================================================

books = pd.read_csv("data/cleaned/books_cleaned.csv")

users = pd.read_csv("data/cleaned/users_cleaned.csv")

borrowings = pd.read_csv(
    "data/cleaned/borrowings_cleaned.csv"
)


# ==========================================================
# ANALYSIS 1: MOST BORROWED BOOKS
# ==========================================================

# Count how many times each book has been borrowed
book_borrow_counts = (
    borrowings
    .groupby("book_id")
    .size()
    .reset_index(name="times_borrowed")
)

# Add the book names
book_borrow_counts = book_borrow_counts.merge(
    books[["book_id", "name"]],
    on="book_id"
)

# Sort from most borrowed to least borrowed
book_borrow_counts = book_borrow_counts.sort_values(
    "times_borrowed",
    ascending=False
)


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

print("=" * 60)
print("MOST BORROWED BOOKS")
print("=" * 60)

print(book_borrow_counts.to_string(index=False))

# ==========================================================
# ANALYSIS 2: LOW UTILISATION BOOKS
# ==========================================================

# Add books that have never been borrowed
all_books = books[["book_id", "name"]].copy()

book_utilisation = all_books.merge(
    book_borrow_counts[["book_id", "times_borrowed"]],
    on="book_id",
    how="left"
)

# Books with no borrowing records have zero borrowings
book_utilisation["times_borrowed"] = (
    book_utilisation["times_borrowed"]
    .fillna(0)
    .astype(int)
)

# Sort from least borrowed to most borrowed
low_utilisation = book_utilisation.sort_values(
    "times_borrowed",
    ascending=True
)


# ==========================================================
# DISPLAY LOW UTILISATION BOOKS
# ==========================================================

print("\n" + "=" * 60)
print("LOW UTILISATION BOOKS")
print("=" * 60)

print(low_utilisation.to_string(index=False))

# ==========================================================
# ANALYSIS 3: MONTHLY BORROWING ACTIVITY
# ==========================================================

# Convert borrow_date to datetime
borrowings["borrow_date"] = pd.to_datetime(borrowings["borrow_date"])

# Extract the month from the borrowing date
borrowings["month"] = borrowings["borrow_date"].dt.month

# Count borrowings per month
monthly_borrowings = (
    borrowings
    .groupby("month")
    .size()
    .reset_index(name="total_borrowings")
)

# Sort by month
monthly_borrowings = monthly_borrowings.sort_values("month")


# ==========================================================
# DISPLAY MONTHLY BORROWING ACTIVITY
# ==========================================================

print("\n" + "=" * 60)
print("MONTHLY BORROWING ACTIVITY")
print("=" * 60)

print(monthly_borrowings.to_string(index=False))

# ==========================================================
# VISUALISATION 1: MONTHLY BORROWINGS
# ==========================================================

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.plot(
    monthly_borrowings["month"],
    monthly_borrowings["total_borrowings"],
    marker="o"
)

plt.title("Monthly Library Borrowing Activity")
plt.xlabel("Month")
plt.ylabel("Number of Borrowings")

plt.xticks(
    [1, 2, 3, 4, 5, 6],
    ["January", "February", "March", "April", "May", "June"]
)

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig("visualisations/monthly_borrowings.png", dpi=300)

plt.show()

# ==========================================================
# ANALYSIS 4: LATE RETURNS
# ==========================================================

# Calculate days late
borrowings["due_date"] = pd.to_datetime(borrowings["due_date"])
borrowings["date_returned"] = pd.to_datetime(borrowings["date_returned"])

borrowings["days_late"] = (
    borrowings["date_returned"] - borrowings["due_date"]
).dt.days

# Ensure early returns have zero days late
borrowings["days_late"] = borrowings["days_late"].clip(lower=0)

# Identify late returns
late_returns = borrowings[borrowings["days_late"] > 0].copy()


# ==========================================================
# DISPLAY LATE RETURNS
# ==========================================================

print("\n" + "=" * 60)
print("LATE RETURNS")
print("=" * 60)

print("Total borrowing transactions:", len(borrowings))
print("Late returns:", len(late_returns))

# Calculate percentage of borrowing transactions returned late
late_return_percentage = (len(late_returns) / len(borrowings)) * 100

print(
    f"Late return percentage: {late_return_percentage:.2f}%"
)

print("\nLate return details:")

print(
    late_returns[
        [
            "borrowing_id",
            "user_id",
            "book_id",
            "due_date",
            "date_returned",
            "days_late"
        ]
    ].to_string(index=False)
)
# ==========================================================
# ANALYSIS 5: MOST ACTIVE USERS
# ==========================================================

# Count how many books each user has borrowed
user_borrow_counts = (
    borrowings
    .groupby("user_id")
    .size()
    .reset_index(name="times_borrowed")
)

# Add user names
user_borrow_counts = user_borrow_counts.merge(
    users[["user_id", "name"]],
    on="user_id"
)

# Sort users from highest to lowest
user_borrow_counts = user_borrow_counts.sort_values(
    "times_borrowed",
    ascending=False
)

# ==========================================================
# DISPLAY USER BORROWING FREQUENCY
# ==========================================================

print("\n" + "=" * 60)
print("MOST ACTIVE USERS")
print("=" * 60)

print(
    user_borrow_counts[
        ["user_id", "name", "times_borrowed"]
    ].to_string(index=False)
)

# ==========================================================
# ANALYSIS 6: PENALTY RATE
# ==========================================================

# Assume a penalty is generated when a book is returned late
penalties = borrowings[borrowings["days_late"] > 0].copy()

# Calculate penalty rate
penalty_rate = (len(penalties) / len(borrowings)) * 100

# Calculate total penalty days
total_penalty_days = penalties["days_late"].sum()

# Calculate average days late
average_days_late = penalties["days_late"].mean()

# ==========================================================
# DISPLAY PENALTY ANALYSIS
# ==========================================================

print("\n" + "=" * 60)
print("PENALTY ANALYSIS")
print("=" * 60)

print("Total borrowing transactions:", len(borrowings))
print("Transactions resulting in penalties:", len(penalties))
print(f"Penalty rate: {penalty_rate:.2f}%")
print("Total penalty days:", total_penalty_days)
print(f"Average days late: {average_days_late:.2f}")

# ==========================================================
# ANALYSIS 7: BOOK DEMAND AND INVENTORY
# ==========================================================

# Start with all books so books with zero borrowings are included
book_demand = books[
    ["book_id", "name", "quantity", "available"]
].copy()

# Add borrowing frequency
book_demand = book_demand.merge(
    book_borrow_counts[
        ["book_id", "times_borrowed"]
    ],
    on="book_id",
    how="left"
)

# Replace missing borrowing counts with zero
book_demand["times_borrowed"] = (
    book_demand["times_borrowed"]
    .fillna(0)
    .astype(int)
)

# Calculate percentage of copies currently unavailable
book_demand["borrowed_copy_percentage"] = (
    (book_demand["quantity"] - book_demand["available"])
    / book_demand["quantity"]
) * 100

# Sort by borrowing frequency
book_demand = book_demand.sort_values(
    "times_borrowed",
    ascending=False
)

# ==========================================================
# DISPLAY BOOK DEMAND
# ==========================================================

print("\n" + "=" * 60)
print("BOOK DEMAND AND INVENTORY")
print("=" * 60)

print(
    book_demand[
        [
            "book_id",
            "name",
            "times_borrowed",
            "quantity",
            "available",
            "borrowed_copy_percentage"
        ]
    ].to_string(index=False)
)

# ==========================================================
# VISUALISATION 1: MOST BORROWED BOOKS
# ==========================================================

import matplotlib.pyplot as plt

# Sort books from lowest to highest for a horizontal bar chart
popular_books = book_demand.sort_values(
    "times_borrowed",
    ascending=True
)

plt.figure(figsize=(10, 6))

plt.barh(
    popular_books["name"],
    popular_books["times_borrowed"]
)

plt.title("Most Borrowed Books")
plt.xlabel("Number of Borrowings")
plt.ylabel("Book")

plt.tight_layout()

# Save the chart
plt.savefig(
    "visualisations/popular_books.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================================
# VISUALISATION 2: LATE RETURNS
# ==========================================================

# Sort late returns by number of days late
late_returns_chart = late_returns.sort_values(
    "days_late",
    ascending=True
)

plt.figure(figsize=(10, 6))

plt.barh(
    late_returns_chart["borrowing_id"].astype(str),
    late_returns_chart["days_late"]
)

plt.title("Late Returns by Borrowing Transaction")
plt.xlabel("Days Late")
plt.ylabel("Borrowing ID")

plt.tight_layout()

# Save the chart
plt.savefig(
    "visualisations/late_returns.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================================
# VISUALISATION 3: PENALTIES
# ==========================================================

# Calculate on-time returns
on_time_returns = len(borrowings) - len(penalties)

# Create summary data
penalty_summary = pd.DataFrame({
    "Return Status": [
        "On-Time Returns",
        "Late Returns"
    ],
    "Number of Transactions": [
        on_time_returns,
        len(penalties)
    ]
})

plt.figure(figsize=(8, 6))

plt.bar(
    penalty_summary["Return Status"],
    penalty_summary["Number of Transactions"]
)

plt.title("On-Time vs Late Library Returns")
plt.xlabel("Return Status")
plt.ylabel("Number of Transactions")

plt.tight_layout()

# Save the chart
plt.savefig(
    "visualisations/penalties.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()