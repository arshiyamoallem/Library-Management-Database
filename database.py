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

            INSERT INTO Books VALUES ('978-0060935467', 'To Kill a Mockingbird', '1960-07-11', 3);
            INSERT INTO Books VALUES ('978-0743273565', 'The Great Gatsby', '1925-04-10', 2); 
            INSERT INTO Books VALUES ('978-0747532699', 'Harry Potter and the Philosopher''s Stone', '1997-06-26', 3); 
            INSERT INTO Books VALUES ('978-0810993136', 'Diary of a Wimpy Kid', '2007-04-01', 4); 
            INSERT INTO Books VALUES ('978-0810994737', 'Diary of a Wimpy Kid: Rodrick Rules', '2008-02-01', 2); 
            INSERT INTO Books VALUES ('978-0141182704', 'Animal Farm: A Fairy Story', '1945-08-17', 2); 

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
                                 
            INSERT INTO Patrons (name, email, password) VALUES ('Joe Smith', 'joe@gmail.com', '123456');
            INSERT INTO Patrons (name, email, password) VALUES ('Alice McDonald', 'alice@gmail.com', '$$password$$');
            INSERT INTO Patrons (name, email, password) VALUES ('Tahle Ghodrati', 'Tahle@gmail.com', 'steve123');

            INSERT INTO Authorship VALUES ('978-0060935467', 1);
            INSERT INTO Authorship VALUES ('978-0743273565', 2);  
            INSERT INTO Authorship VALUES ('978-0747532699', 3);
            INSERT INTO Authorship VALUES ('978-0810993136', 4);                             
            INSERT INTO Authorship VALUES ('978-0810994737', 4);
            INSERT INTO Authorship VALUES ('978-0141182704', 5);  

            INSERT INTO Categorization VALUES ('978-0060935467', 1);
            INSERT INTO Categorization VALUES ('978-0060935467', 2);
            INSERT INTO Categorization VALUES ('978-0743273565', 1);     
            INSERT INTO Categorization VALUES ('978-0743273565', 2);                             
            INSERT INTO Categorization VALUES ('978-0747532699', 1);
            INSERT INTO Categorization VALUES ('978-0747532699', 3);
            INSERT INTO Categorization VALUES ('978-0810993136', 1); 
            INSERT INTO Categorization VALUES ('978-0810993136', 4);
            INSERT INTO Categorization VALUES ('978-0810994737', 1);
            INSERT INTO Categorization VALUES ('978-0810994737', 4);
            INSERT INTO Categorization VALUES ('978-0141182704', 1);                                   
            INSERT INTO Categorization VALUES ('978-0141182704', 5);              

            INSERT INTO Circulation VALUES (1, '978-0747532699', '2026-01-01','2026-01-15','2026-01-14');
            INSERT INTO Circulation VALUES (1, '978-0141182704', '2026-02-01','2026-02-15', NULL);
            INSERT INTO Circulation VALUES (2, '978-0743273565', '2026-03-25','2026-04-01', NULL);
            INSERT INTO Circulation VALUES (3, '978-0810993136', '2026-04-01','2026-04-15', '2026-04-14');
            
                                 
            INSERT INTO SystemLogs (log_date, description, error_type, patron_id)
            VALUES ('2026-03-15', 'Book listed as available but was not on shelf', 'Inventory Error', 1);
            INSERT INTO SystemLogs (log_date, description, error_type, patron_id)
            VALUES ('2026-03-28', 'Wrong genre tag on Animal Farm', 'Cataloging Error', 2);
            """)
            conn.commit()
            conn.close()
        
        def get_all_genres(self):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT genre_id, genre_name FROM Genres ORDER BY genre_name ASC")
            results = cursor.fetchall()
            conn.close()
            return results

        def get_book_details(self, isbn):
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT b.title, b.pub_date, b.copy_count FROM Books b WHERE b.isbn = ?", (isbn,))
            book = cursor.fetchone()
            
            cursor.execute("""
                SELECT a.name
                FROM Authors a
                JOIN Authorship au ON a.author_id = au.author_id
                WHERE au.isbn = ?
            """, (isbn,))
            authors = cursor.fetchall()

            conn.close()
            return book, authors
        
        def get_all_patrons(self):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT patron_id, name, email FROM Patrons ORDER BY name ASC")
            results = cursor.fetchall()
            conn.close()
            return results
        
        def get_patron_by_id(self, patron_id):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT patron_id, name, email FROM Patrons WHERE patron_id = ?", (patron_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        
        def get_book_by_isbn(self, isbn):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT isbn, title, pub_date, copy_count FROM Books WHERE isbn = ?", (isbn,))
            result = cursor.fetchone()
            conn.close()
            return result
        
        def get_active_loans(self, patron_id):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.isbn, b.title, c.borrow_date, c.due_date
                FROM Circulation c
                JOIN Books b ON c.isbn = b.isbn
                WHERE c.patron_id = ? AND c.return_date IS NULL
                ORDER BY c.borrow_date ASC
            """, (patron_id,))
            results = cursor.fetchall()
            conn.close()
            return results

        def search_books_by_genre(self, genre_id):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.isbn, b.title, b.pub_date, b.copy_count
                FROM Books b
                JOIN Categorization c ON b.isbn = c.isbn
                WHERE c.genre_id = ?
                ORDER BY b.title ASC
            """, (genre_id,))
            results = cursor.fetchall()
            conn.close()
            return results

        def search_books_by_author(self, author_name):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.isbn, b.title, b.pub_date, b.copy_count, a.name
                FROM Books b
                JOIN Authorship au ON b.isbn = au.isbn
                JOIN Authors a ON au.author_id = a.author_id
                WHERE a.name LIKE ?
                ORDER BY b.title ASC
            """, (f"%{author_name}%",))
            results = cursor.fetchall()
            conn.close()
            return results

        def check_book_availability(self, title):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.isbn, b.title, b.pub_date, b.copy_count
                FROM Books b
                WHERE title LIKE ?
                ORDER BY title ASC
            """, (f"%{title}%",))
            results = cursor.fetchall()
            conn.close()
            return results
        
        def get_borrowing_history(self, patron_id):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.title, c.borrow_date, c.due_date, c.return_date
                FROM Circulation c
                JOIN Books b ON c.isbn = b.isbn
                WHERE c.patron_id = ?
                ORDER BY c.borrow_date ASC
            """, (patron_id,))
            results = cursor.fetchall()
            conn.close()
            return results

        def get_overdue_books(self):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.name, b.title, c.borrow_date, c.due_date
                FROM Circulation c
                JOIN Patrons p ON c.patron_id = p.patron_id
                JOIN Books b ON c.isbn = b.isbn
                WHERE c.return_date IS NULL AND c.due_date < date('now')
                ORDER BY c.due_date ASC
            """)
            results = cursor.fetchall()
            conn.close()
            return results

        def borrow_book(self, patron_id, isbn, borrow_date, due_date):
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO Circulation (patron_id, isbn, borrow_date, due_date, return_date)
                    VALUES (?, ?, ?, ?, NULL)
                """, (patron_id, isbn, borrow_date, due_date))
                cursor.execute("UPDATE Books SET copy_count = copy_count - 1 WHERE isbn = ?", (isbn,))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error borrowing book: {e}")
                return False
            finally:
                conn.close()

        def return_book(self, patron_id, isbn, borrow_date, return_date):
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE Circulation
                    SET return_date = ?
                    WHERE patron_id = ? AND isbn = ? AND borrow_date = ? AND return_date IS NULL
                """, (return_date, patron_id, isbn, borrow_date))
                cursor.execute("UPDATE Books SET copy_count = copy_count + 1 WHERE isbn = ?", (isbn,))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error returning book: {e}")
                return False
            finally:
                conn.close()

        def report_system_issue(self, patron_id, log_date, description, error_type):
            conn = self.get_connection()
            cursor = conn.cursor() 
            try: 
                cursor.execute("""
                    INSERT INTO SystemLogs (log_date, description, error_type, patron_id)
                    VALUES (?, ?, ?, ?)
                """, (log_date, description, error_type, patron_id))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error reporting system issue: {e}")
                return False
            finally:
                conn.close()
    