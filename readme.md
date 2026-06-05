# Library-Management-Database 

## DATABASE FILENAME & LOCATION 
Filename: library.db

Location: Root directory [Library-Management-Database] 
(the same folder as main.py and database.py)

Open with sqlite3 command line:
sqlite3 "Library-Management-Database/library.db"

Note: The database is pre-seeded with sample patrons, books, 
authors, genres, and circulation history for demonstration.

## HOW TO RUN THE PROGRAM 
1. Open a terminal/command prompt in the project folder.
2. Run the command: python main.py
3. Follow the custom on-screen menu to interact with the database.

## PROJECT OVERVIEW 
This project is a Library Management Database System using 
raw SQL wrapped in a Python CLI. 

It demonstrates N:N relationships (Circulation, Authorship, Categorization) 
and 1:N reporting logic.
