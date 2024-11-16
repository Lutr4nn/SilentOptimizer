from menu import terminal_menu
import time

def main():
    while True:
        terminal_menu()   
        if input("Do you want to continue? (y/n): ").lower() != "y":
            print("Goodbye!")   
            time.sleep(2)
            exit()
         
    
if __name__ == "__main__":
    main()
    
    