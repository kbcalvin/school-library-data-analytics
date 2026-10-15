# School Library Data Analytics

## Project Overview

This project analyses school library borrowing records to understand book demand, borrowing patterns, inventory availability, and late returns. It demonstrates how data analytics can support evidence-based decisions in library management.

**Note:** This project uses a synthetic sample dataset created for learning and portfolio demonstration. It does not contain real school records.

## Business Questions

The analysis investigates:

1. Which books are borrowed most frequently?
2. Which books have low utilisation?
3. How does borrowing activity vary by month?
4. How many borrowing transactions involve late returns?
5. Which users borrow books most frequently?
6. What percentage of borrowing transactions involve late returns?
7. How do book demand and inventory availability compare?

## Tools and Technologies

- **Python:** Data cleaning and analysis
- **Pandas:** Data manipulation and analysis
- **Matplotlib:** Data visualisation
- **SQL / MySQL:** Relational data analysis
- **phpMyAdmin:** Database management
- **Git and GitHub:** Version control and project sharing

## Project Structure

```text
school-library-data-analytics/
├── data/
│   ├── books.csv
│   ├── users.csv
│   └── borrowings.csv
├── sql/
│   └── analysis_queries.sql
├── python/
│   ├── data_cleaning.py
│   └── analysis.py
├── visualisations/
│   ├── popular_books.png
│   ├── monthly_borrowings.png
│   ├── late_returns.png
│   └── penalties.png
├── requirements.txt
└── README.md
```

## Dataset

The sample dataset contains:

- 10 books
- 15 users
- 30 borrowing transactions

The dataset covers January to June 2026.

## Analysis Process

1. **Data preparation:** Loaded the CSV files and checked missing values, duplicates, data types, and borrowing dates.
2. **SQL analysis:** Used joins, aggregations, conditional expressions, date functions, and sorting to answer the business questions.
3. **Python analysis:** Used Pandas to calculate borrowing frequencies, monthly activity, late returns, and inventory indicators.
4. **Visualisation:** Created charts to communicate the results.
5. **Recommendations:** Interpreted the findings to identify possible improvements to library operations.

## Key Findings

- **Most borrowed book:** Mathematics for Secondary Schools, with 7 borrowing transactions.
- **Second most borrowed book:** Introduction to Computer Science, with 5 transactions.
- **Lowest utilisation:** History of Zimbabwe had no recorded borrowing transactions.
- **Monthly activity:** There were 5 transactions in each month from January to June 2026.
- **Late returns:** 11 of 30 transactions involved late returns, representing 36.67%.
- **User activity:** Each of the 15 users had 2 recorded borrowing transactions.
- **Inventory indicator:** Computer Programming Basics had 2 available copies out of 8, while Mathematics for Secondary Schools had 8 available copies out of 15.

These findings describe the synthetic sample data and should not be interpreted as evidence about an actual school's library.

## Recommendations

1. Review demand for Mathematics for Secondary Schools and assess whether the current number of copies meets users' needs.
2. Monitor the availability of Computer Programming Basics and review its borrowing history before deciding whether more copies are needed.
3. Investigate why History of Zimbabwe had no recorded borrowing transactions. Consider visibility, relevance, and user interest before making stock decisions.
4. Consider reminders before due dates to help reduce late returns.
5. Monitor borrowing and availability trends over a longer period before making major purchasing decisions.

## How to Run the Python Analysis

### 1. Clone the repository

```bash
git clone https://github.com/kbcalvin/school-library-data-analytics.git
cd school-library-data-analytics
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the scripts

```powershell
python python/data_cleaning.py
python python/analysis.py
```

The project also includes SQL queries in `sql/analysis_queries.sql`, which can be run against a MySQL database populated with the supplied CSV data.

## Future Improvements

- Build an interactive Power BI dashboard.
- Add more visualisations and comparative metrics.
- Expand the dataset to analyse longer-term trends.
- Develop automated data-quality checks.
- Improve reporting of inventory demand and late returns.

## Power BI Dashboard

An interactive Power BI dashboard was developed to analyse school library borrowing activity, book availability, and late returns.

### Dashboard Preview

![School Library Analytics Dashboard](powerbi/dashboard.png)

### Key Performance Indicators

| Metric | Result |
|---|---:|
| Total Borrowings | 30 |
| Total Book Titles | 10 |
| Total Users | 15 |
| Late Return Rate | 36.67% |

### Dashboard Features

- **Most Borrowed Books:** Identifies the most frequently borrowed textbooks.
- **Monthly Borrowing Activity:** Displays borrowing trends from January to June 2026.
- **Book Inventory Availability:** Compares available and unavailable copies.
- **On-Time vs Late Returns:** Shows the proportion of borrowing transactions returned late.
- **Interactive Book Filter:** Allows users to explore statistics for individual books.

### Key Insights

- Mathematics for Secondary Schools was the most borrowed title, with 7 borrowing transactions.
- Introduction to Computer Science ranked second, with 5 transactions.
- Monthly borrowing activity remained constant at 5 transactions per month.
- 11 out of 30 borrowing transactions were returned late, representing 36.67%.
- Computer Programming Basics had 2 available copies out of 8, suggesting that its stock availability may need further investigation.

### Recommendations

1. Monitor demand for frequently borrowed textbooks before making purchasing decisions.
2. Introduce automated reminders to help reduce late returns.
3. Review inventory availability regularly to identify potential shortages.
4. Promote books with low borrowing activity.

### Power BI Report

[Open the Power BI Report](powerbi/School_Library_Analytics.pbix)

**Dataset note:** This project uses synthetic sample data for educational and portfolio demonstration purposes.

## Author

**Kudakwashe Calvin Bamusi**

BSc Information Technology Graduate | Aspiring Data Analyst

- GitHub: [kbcalvin](https://github.com/kbcalvin/)
- Email: kbcalvin27@gmail.com