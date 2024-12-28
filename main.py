from option1 import option1
from option2 import option2

def main():
    print("\nSelect an option:")
    print("1. Move emails from a sender to 'EmailTracker/Unsubscribe' and create a filter.")
    print("2. Create a new folder for selected senders and filter future emails.")

    try:
        choice = int(input("\nEnter your choice: "))
        if choice == 1:
            option1()
        elif choice == 2:
            option2()
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == '__main__':
    main()
