"""
Student Name: Arshiya Moallem
Student Number: 101324189

Final SQlite Project 
Library Database Management System - UI Layer 
"""

import time, sys
from datetime import datetime
from database import LibraryDB

class library_database_hub:
    def __init__(self):
        self.db = LibraryDB()

    # --- LOADING ANIMATION ---

    def loading_animation(self, text: str) -> None:
        for _ in range(3):
            for dot_count in range(1, 4):  
                sys.stdout.write(f"\r{text}{'.' * dot_count}")  # Overwrite the line with dots
                sys.stdout.flush()  
                time.sleep(0.5)  
                sys.stdout.write("\r" + text + "   ")  
                sys.stdout.flush()  
        sys.stdout.write("\r" + " " * len(text))  
        sys.stdout.flush() 
        print()   

    # --- DISPLAY MENU ---

    def display_menu(self) -> None:
        """Print the main hub menu."""
        print("\n===============================")
        print("  LIBRARY MANAGEMENT DATABASE ")
        print("===============================")
        print("1- Search Books by Genre")
        print("2- Search Books by Author") 
        print("3- View Borrowing Books")
        print("4- Check Book Availability")
        print("5- View Overdue Books") 
        print("6- Borrow a Book")
        print("7- Return a Book")
        print("8- Report System Issue") 
        print("9- Who is the creator of this program?")  
        print("10- Exit")     
        print("===============================")

    # --- MENU OPTION METHODS ---

    def search_book_by_genres(self) -> None:
        print("\n--- Search Books by Genre ---")
 
        genres = self.db.get_all_genres()
        if not genres:
            print("No genres found.")
            return
 
        print("\nAvailable Genres:")
        for g in genres:
            print(f"  [{g[0]}] {g[1]}")
 
        try:
            genre_id = int(input("\nEnter Genre ID: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
 
        books = self.db.search_books_by_genre(genre_id)
 
        if not books:
            print("No books found for that genre.")
            return
 
        print(f"\n{'ISBN':<25} {'Title':<40} {'Published':<12} {'Copies'}")
        print("-" * 85)
        for b in books:
            print(f"{b[0]:<25} {b[1]:<40} {b[2]:<12} {b[3]}")
 
        isbn = input("\nEnter an ISBN to view its authors and details (or press Enter to skip): ").strip()
        if isbn:
            book, authors = self.db.get_book_details(isbn)
            if book:
                print(f"\nTitle:            {book[0]}")
                print(f"Published:        {book[1]}")
                print(f"Copies Available: {book[2]}")
                print(f"Authors:          {', '.join([a[0] for a in authors]) if authors else 'N/A'}")
            else:
                print("ISBN not found.")

    def search_book_by_author(self) -> None:
        print("\n--- Search Books by Author ---")
        author_name = input("Enter author name: ").strip()
 
        results = self.db.search_books_by_author(author_name)
 
        if not results:
            print("No books found for that author.")
            return
 
        print(f"\n{'ISBN':<25} {'Title':<40} {'Published':<12} {'Copies':<8} {'Author'}")
        print("-" * 100)
        for r in results:
            print(f"{r[0]:<25} {r[1]:<40} {r[2]:<12} {r[3]:<8} {r[4]}")


    def view_borrowing_history(self) -> None:
        print("\n--- View Patron Borrowing History ---")
 
        patrons = self.db.get_all_patrons()
        print("\nRegistered Patrons:")
        for p in patrons:
            print(f"  [{p[0]}] {p[1]} ({p[2]})")
 
        try:
            patron_id = int(input("\nEnter Patron ID: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
 
        history = self.db.get_borrowing_history(patron_id)
 
        if not history:
            print("No borrowing history found for this patron.")
            return
 
        print(f"\n{'Title':<40} {'Borrowed':<12} {'Due':<12} {'Returned'}")
        print("-" * 80)
        for h in history:
            returned = h[3] if h[3] else "Not yet returned"
            print(f"{h[0]:<40} {h[1]:<12} {h[2]:<12} {returned}")


    def check_book_availability(self) -> None:
        print("\n--- Check Book Availability ---")
        title = input("Enter book title (or part of it): ").strip()
 
        results = self.db.check_book_availability(title)
 
        if not results:
            print("No books found.")
            return
 
        print(f"\n{'ISBN':<25} {'Title':<40} {'Published':<12} {'Copies Available'}")
        print("-" * 90)
        for r in results:
            print(f"{r[0]:<25} {r[1]:<40} {r[2]:<12} {r[3]}")


    def view_overdue_books(self) -> None:
        print("\n--- Overdue Books ---")
 
        results = self.db.get_overdue_books()
 
        if not results:
            print("No overdue books at this time.")
            return
 
        print(f"\n{'Patron':<20} {'Title':<40} {'Borrowed':<12} {'Due Date'}")
        print("-" * 110)
        for r in results:
            print(f"{r[0]:<20} {r[1]:<40} {r[2]:<12} {r[3]}")


    def borrow_book(self) -> None:
        print("\n--- Borrow a Book ---")
 
        try:
            patron_id = int(input("Enter your Patron ID: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
 
        patron = self.db.get_patron_by_id(patron_id)
        if not patron:
            print("Patron not found.")
            return
 
        print(f"Welcome, {patron[1]}!")
        isbn = input("Enter the ISBN of the book you want to borrow: ").strip()
 
        book = self.db.get_book_by_isbn(isbn)
        if not book:
            print("Book not found.")
            return
 
        if book[3] <= 0:
            print(f"Sorry, '{book[1]}' is currently unavailable.")
            return
 
        borrow_date = input("Enter borrow date (YYYY-MM-DD): ").strip()
        due_date = input("Enter due date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(borrow_date, "%Y-%m-%d")
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
 
        success = self.db.borrow_book(patron_id, isbn, borrow_date, due_date)
        if success:
            print(f"\nSuccessfully borrowed '{book[1]}'!")
            print(f"Due date: {due_date}")

    def return_book(self) -> None:        
        print("\n--- Return a Book ---")
 
        try:
            patron_id = int(input("Enter your Patron ID: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
 
        loans = self.db.get_active_loans(patron_id)
        if not loans:
            print("No active loans found for this patron.")
            return
 
        print("\nCurrently borrowed books:")
        for i, loan in enumerate(loans):
            print(f"  [{i + 1}] {loan[1]} (ISBN: {loan[0]}, Due: {loan[3]})")
 
        try:
            choice = int(input("\nEnter the number of the book to return: ")) - 1
            if choice < 0 or choice >= len(loans):
                raise ValueError
        except ValueError:
            print("Invalid selection.")
            return
 
        selected = loans[choice]
        return_date = input("Enter return date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(return_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
 
        success = self.db.return_book(patron_id, selected[0], selected[2], return_date)
        if success:
            print(f"\nSuccessfully returned '{selected[1]}'!")

    def report_system_issue(self) -> None:
        print("\n--- Report a System Issue ---")
 
        try:
            patron_id = int(input("Enter your Patron ID: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
 
        patron = self.db.get_patron_by_id(patron_id)
        if not patron:
            print("Patron not found.")
            return
 
        print("\nError Types:")
        print("  1 - Inventory Error")
        print("  2 - Cataloging Error")
        print("  3 - System Error")
        print("  4 - Other")
 
        error_types = {1: "Inventory Error", 2: "Cataloging Error", 3: "System Error", 4: "Other"}
        try:
            error_choice = int(input("Select error type: ").strip())
            error_type = error_types.get(error_choice, "Other")
        except ValueError:
            error_type = "Other"
 
        description = input("Describe the issue: ").strip()
        log_date = input("Enter date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(log_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
 
        success = self.db.report_system_issue(patron_id, log_date, description, error_type)
        if success:
            print("\nYour report has been submitted successfully. Thank you!")

    def creator_info(self) -> None:
        self.loading_animation("Loading Creator Info") 
        print("Arshiya Moallem\nSoftware Engineer - Carleton University\n")
    
    # --- MAIN PROGRAM LOOP ---
    
    def run(self) -> None: 
        while True:
            self.display_menu()
            try:
                choice = int(input("Your choice: ").strip())
                print("")

                if choice == 1:
                    self.search_book_by_genres()
                
                elif choice == 2:
                    self.search_book_by_author()
                
                elif choice == 3: 
                    self.view_borrowing_history()
                
                elif choice == 4:
                    self.check_book_availability()
                
                elif choice == 5: 
                    self.view_overdue_books()
                
                elif choice == 6:
                    self.borrow_book()
                
                elif choice == 7: 
                    self.return_book()
                
                elif choice == 8:
                    self.report_system_issue()
                
                elif choice == 9:
                    time.sleep(1)
                    self.creator_info()  

                elif choice == 10:
                    self.loading_animation("Exiting Program") 
                    print("Thank you for using this program! Goodbye!\n")
                    break  
                
                else:
                    print("Invalid menu option! Choose 1-10.\n")

            except ValueError:
                print("Invalid input. Please enter a number.\n")

            except Exception as e:
                print(f"An unexpected error occured: {e}")

if __name__ == "__main__":
    lib_hub = library_database_hub()
    lib_hub.run()

#end