"""
Final SQlite Project 
Library Database
"""
import time, sys

class GameHub:
    def __init__(self):
        self.sqlfiles = {
        }
        
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
    
    def display_menu(self) -> None:
        """Print the main hub menu."""
        print("\nLibrary Database")
        print("_______________________________________")
        print("1- ___")
        print("2- ___") 
        print("3- ___")
        print("4- Who is the creator of this program?")  
        print("5- Exit")     
        print("_______________________________________")

    def run(self) -> None: 
        while True:
            self.display_menu()
            try:
                choice = int(input("Your choice: ").strip())
                print("\n")

                if choice in self.sqlfiles:
                    #file = self.sqlfiles[choice]()
                    #game.play()
                    self.loading_animation("Returning back to hub") 

                elif choice == 4:
                    time.sleep(1)
                    print("Arshiya Moallem\nSoftware Engineer\nStudent Number: 101324189\n")
                    break  

                elif choice == 5:
                    self.loading_animation("Exiting Program") 
                    print("Thank you for using this program! Goodbye!\n")
                    break  
                
                else:
                    print("Invalid menu option! Choose 1-5.\n")

            except ValueError:
                print("Unknown Entry. Try again")
if __name__ == "__main__":
    game_hub = GameHub()
    game_hub.run()