"""
Student Name: Arshiya Moallem
Student Number: 101324189

Final SQlite Project 
Library Database Management System - UI Layer 
"""

import time, sys
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

    def run(self) -> None: 
        while True:
            self.display_menu()
            try:
                choice = int(input("Your choice: ").strip())
                print("")

                if choice == 1:
                    self.search_catalog()
                
                elif choice == 2:
                    self.report_issue()
                
                elif choice == 3: 
                    self.view_borrowing_books()
                
                elif choice == 4:
                    self.report_issue()
                
                elif choice == 5: 
                    self.view_borrowing_books()
                
                elif choice == 6:
                    self.report_issue()
                
                elif choice == 7: 
                    self.view_borrowing_books()
                
                elif choice == 8:
                    self.report_issue()
                
                elif choice == 9:
                    time.sleep(1)
                    LibraryDB.creator_info(self)  

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