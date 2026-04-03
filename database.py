"""
Student Name: Arshiya Moallem
Student Number: 101324189

Final SQlite Project 
Library Database Management System - Database Layer 
"""

import sqlite3
import sys

class LibraryDB:

        def __init__(self):
            self.db_name = "library.db"
            self.set_up_tables()
            self.insert_sample_data()

        def get_connection(self):
            try:
                conn = sqlite3.connect(self.db_name)
                conn.execute("PRAGMA foreign_keys = ON")
                return conn
            except sqlite3.Error as e:
                print(f"Database connection error: {e}")
                sys.exit(1)
        
        def set_up_tables(self):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executescript("""

            CREATE TABLE IF NOT EXISTS Books (
                isbn        TEXT PRIMARY KEY,
                title       TEXT NOT NULL,
                pub_date    TEXT,
                copy_count  INTEGER DEFAULT 1
            );
 
            CREATE TABLE IF NOT EXISTS Authors (
                author_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL
            );
 
            CREATE TABLE IF NOT EXISTS Genres (
                genre_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                genre_name  TEXT NOT NULL
            );
 
            CREATE TABLE IF NOT EXISTS Patrons (
                patron_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                email       TEXT UNIQUE NOT NULL,
                password    TEXT NOT NULL
            );
 
            CREATE TABLE IF NOT EXISTS SystemLogs (
                log_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                log_date    TEXT NOT NULL,
                description TEXT NOT NULL,
                error_type  TEXT,
                patron_id   INTEGER NOT NULL,
                FOREIGN KEY (patron_id) REFERENCES Patrons(patron_id)
            );
 
            CREATE TABLE IF NOT EXISTS Circulation (
                patron_id   INTEGER NOT NULL,
                isbn        TEXT NOT NULL,
                borrow_date TEXT NOT NULL,
                due_date    TEXT NOT NULL,
                return_date TEXT,
                PRIMARY KEY (patron_id, isbn, borrow_date),
                FOREIGN KEY (patron_id) REFERENCES Patrons(patron_id),
                FOREIGN KEY (isbn) REFERENCES Books(isbn)
            );
 
            CREATE TABLE IF NOT EXISTS Authorship (
                isbn        TEXT NOT NULL,
                author_id   INTEGER NOT NULL,
                PRIMARY KEY (isbn, author_id),
                FOREIGN KEY (isbn) REFERENCES Books(isbn),
                FOREIGN KEY (author_id) REFERENCES Authors(author_id)
            );
 
            CREATE TABLE IF NOT EXISTS Categorization (
                isbn        TEXT NOT NULL,
                genre_id    INTEGER NOT NULL,
                PRIMARY KEY (isbn, genre_id),
                FOREIGN KEY (isbn) REFERENCES Books(isbn),
                FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
            );

            """)
            conn.commit()
            conn.close()

        def insert_sample_data(self):
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Books")
            if cursor.fetchone()[0] > 0:
                conn.close()
                return
            
            cursor.executescript(""" 

            INSERT INTO Books VALUES (978-0060935467, 'To Kill a Mockingbird', 1960-07-11, 3);
            INSERT INTO Books VALUES (978-0743273565, 'The Great Gatsby', 1925-04-10, 2); 
            INSERT INTO Books VALUES (978-0747532699, 'Harry Potter and the Philosopher's Stone', 1997-06-26, 3); 
            INSERT INTO Books VALUES (978-0810993136, 'Diary of a Wimpy Kid', 2007-04-01, 4); 
            INSERT INTO Books VALUES (978-0810994737, 'Diary of a Wimpy Kid', 2008-02-01, 2); 
            INSERT INTO Books VALUES (978-0141182704, 'Animal Farm: A Fairy Story', 1945-08-17, 2); 

            INSERT INTO Authors (name) VALUES ('Harper Lee');
            INSERT INTO Authors (name) VALUES ('F. Scott Fitzgerald');
            INSERT INTO Authors (name) VALUES ('J.K. Rowling');
            INSERT INTO Authors (name) VALUES ('Jeff Kinney');
            INSERT INTO Authors (name) VALUES ('George Orwell');

            INSERT INTO Genres (genre_name) VALUES ('Fiction');
            INSERT INTO Genres (genre_name) VALUES ('Tragedy');
            INSERT INTO Genres (genre_name) VALUES ('Fantasy');
            INSERT INTO Genres (genre_name) VALUES ('Comedy');
            INSERT INTO Genres (genre_name) VALUES ('Allegory');
                                 
            INSERT INTO Patrons (name, email, password) VALUES (Joe Smith, joe@gmail.com, 123456);
            INSERT INTO Patrons (name, email, password) VALUES (Alice McDonald, alice@gmail.com, $$password$$);
            INSERT INTO Patrons (name, email, password) VALUES (Esfandiar Ghodrati, esfandiar@gmail.com, steve123);

            INSERT INTO Authorship VALUES ('978-0060935467-0', 1);
            INSERT INTO Authorship VALUES ('978-0060935467-0', 1);
            INSERT INTO Authorship VALUES ('978-0060935467-0', 1);
            INSERT INTO Authorship VALUES ('978-0060935467-0', 1);
            INSERT INTO Authorship VALUES ('978-0060935467-0', 1);  

            INSERT INTO Categorization VALUES ('978-0060935467-0', 1);
            INSERT INTO Categorization VALUES ('978-0060935467-4', 4);                             
            INSERT INTO Categorization VALUES ('978-0-316-76948-0', 1);
            INSERT INTO Categorization VALUES ('978-0-316-76948-0', 4);  
            INSERT INTO Categorization VALUES ('978-0-316-76948-0', 1);
            INSERT INTO Categorization VALUES ('978-0-316-76948-0', 4);                             
            INSERT INTO Categorization VALUES ('978-0-316-76948-0', 1);
            INSERT INTO Categorization VALUES ('978-0-316-76948-0', 4);                  

            INSERT INTO Circulation VALUES (name, email, password) VALUES (Joe Smith, joe@gmail.com, 123456);
            INSERT INTO Circulation VALUES (name, email, password) VALUES (Joe Smith, joe@gmail.com, 123456);
            INSERT INTO Circulation VALUES (name, email, password) VALUES (Joe Smith, joe@gmail.com, 123456);
            INSERT INTO Circulation VALUES (name, email, password) VALUES (Joe Smith, joe@gmail.com, 123456);
                                 
            """)

        def search_books_by_genre(self):
            pass

        def search_books_by_author(self):
            pass

        def check_book_availability(self):
            pass
        
        def get_borrowing_history(self):
            pass

        def get_overdue_books(self):
            pass

        def borrow_book(self):
            pass

        def return_book(self):
            pass

        def report_system_issue(self):
            pass

        
        def creator_info(self):
            print("Arshiya Moallem\nSoftware Engineer - Carleton University\n")
