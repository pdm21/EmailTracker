import subprocess
from email_auth import authenticate_gmail
from email_utils import fetch_recent_emails
from option1 import option1
from option2 import option2

def run_go_option1_for_multiple_senders(senders):
    """Run the Go program with multiple sender arguments."""
    try:
        # Construct the command to run the Go program
        command = ["go", "run", "go-option1.go"] + senders
        subprocess.run(command)
    except Exception as e:
        print(f"Error running the Go program: {e}")

def main():
    print("\nSelect an option:")
    print("1. Move emails from a sender to 'EmailTracker/Unsubscribe' and create a filter.")
    print("2. Create a new folder for selected senders and filter future emails.")

    try:
        choice = int(input("\nEnter your choice: "))
        if choice == 1:
            print("\nWould you like to complete this process...")
            print("1. For a single sender")
            print("2. For multiple senders (Go program)")
            choice = int(input("\nEnter your choice: "))
            if choice == 1:
                option1()
            elif choice == 2:
                # Authenticate and fetch recent emails
                service = authenticate_gmail()
                emails = fetch_recent_emails(service)

                if not emails:
                    print("No emails found.")
                    return

                # Display the emails as a numbered list
                print("\nSelect senders by entering their corresponding numbers (space-separated):\n")
                senders = {}
                for idx, email in enumerate(emails):
                    sender = email['sender']
                    print(f"{idx + 1}. Sender: {sender}, Subject: {email['subject']}")
                    senders[idx + 1] = sender

                # Get user input for selected numbers
                try:
                    selected_numbers = input("\nEnter numbers for senders: ").split()
                    selected_senders = [senders[int(num)] for num in selected_numbers if int(num) in senders]

                    if not selected_senders:
                        print("No valid senders selected.")
                        return

                    print(f"Running Go program for senders: {', '.join(selected_senders)}")
                    run_go_option1_for_multiple_senders(selected_senders)

                except ValueError:
                    print("Invalid input. Please enter valid numbers.")

            else:
                print("Invalid choice.")
        elif choice == 2:
            option2()
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == '__main__':
    main()
