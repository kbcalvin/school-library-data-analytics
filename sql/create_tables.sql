-- School Library Data Analytics
-- Database Setup Script

CREATE DATABASE IF NOT EXISTS school_library_analytics;

USE school_library_analytics;

CREATE TABLE IF NOT EXISTS books (
    book_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    publisher VARCHAR(255),
    quantity INT NOT NULL,
    available INT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS borrowings (
    borrowing_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    date_returned DATE NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);